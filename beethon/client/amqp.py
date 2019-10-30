import asyncio
import json
import os
import uuid
from time import sleep
from typing import Optional, Any, Tuple, Dict

import aio_pika
from aio_pika import Message

from beethon.client.base import Client
from beethon.exceptions.response_exceptions import ThereIsNoSuchService
from beethon.messages.base import Request, Response


class AMQPClient(Client):

    def __init__(self, service_name: str, timeout: int = 10):
        super().__init__(service_name=service_name)
        self.timeout = timeout

        self.connection: Optional[aio_pika.Connection] = None
        # self.channel: Optional[aio_pika.Channel] = None
        # self.queue: Optional[aio_pika.Queue] = None

        self.loop = asyncio.get_event_loop()

        self._responses: Dict[str, Response] = {}

        self.queue_name = self.service_name

    def _get_settings(self) -> Tuple[str, str, str]:
        host = os.environ.get('AMQP_HOST', 'localhost:5672')
        user = os.environ.get('AMQP_USER', 'guest')
        password = os.environ.get('AMQP_PASSWORD', 'guest')

        return host, user, password

    async def call(self, method_name: str, *args, **kwargs) -> Optional[Any]:
        return await asyncio.wait_for(self._call(method_name, *args, **kwargs), timeout=self.timeout)

    async def _call(self, method_name: str, *args, **kwargs) -> Optional[Any]:
        amqp_host, amqp_user, amqp_pass = self._get_settings()
        self.connection = await aio_pika.connect_robust(
            "amqp://{}:{}@{}/".format(amqp_user, amqp_pass, amqp_host),
            loop=self.loop
        )

        async with self.connection:
            channel = await self.connection.channel()
            queue = await channel.declare_queue(
                self.queue_name,
                auto_delete=False
            )
            request = Request(method_name=method_name, args=args, kwargs=kwargs)
            correlation_id = uuid.uuid4().hex
            message = Message(body=request.serialize().encode(), correlation_id=correlation_id)
            await channel.default_exchange.publish(message=message, routing_key=self.queue_name)

            async with queue.iterator() as queue_iter:
                async for msg in queue_iter:
                    response_dict = json.loads(msg.body)
                    if msg.correlation_id != correlation_id or response_dict.get('message_type') != 'response':
                        print('Got and ignored message')
                        msg.reject(requeue=True)
                        continue
                    async with msg.process():
                        exc = None
                        if response_dict.get('exception'):
                            exc = Exception('')
                        response = Response(
                            result=response_dict['result'],
                            status=int(response_dict['status']),
                            exception=exc
                        )
                        break

            return self.process_response(response)

    async def stop(self):
        pass
