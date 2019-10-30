import asyncio
import json
import os
from time import sleep
from typing import Tuple, Optional

import aio_pika
from aio_pika import IncomingMessage, Message

from beethon.handlers.base import Handler
from beethon.messages.base import Request


class AMQPHandler(Handler):

    def __init__(self, service, **kwargs):
        super().__init__(service)

        self.connection: Optional[aio_pika.Connection] = None
        self.channel: Optional[aio_pika.Channel] = None
        self.loop = asyncio.get_event_loop()

    def _get_settings(self) -> Tuple[str, str, str]:
        host = os.environ.get('AMQP_HOST', 'localhost:5672')
        user = os.environ.get('AMQP_USER', 'guest')
        password = os.environ.get('AMQP_PASSWORD', 'guest')

        return host, user, password

    async def _on_amqp_message(self, msg: IncomingMessage):
        body_dict = json.loads(msg.body)

        method_name = body_dict['method_name']
        args = body_dict['args']
        kwargs = body_dict['kwargs']

        request = Request(method_name=method_name,
                          args=args,
                          kwargs=kwargs)
        response = await self._on_new_request(request)
        serialized_response = response.serialize()
        message = Message(body=serialized_response.encode(), correlation_id=msg.correlation_id)
        await self.channel.default_exchange.publish(message=message, routing_key=self._service.name)

    async def run(self):

        amqp_host, amqp_user, amqp_password = self._get_settings()

        self.connection = await aio_pika.connect_robust(
            "amqp://{}:{}@{}/".format(amqp_user, amqp_password, amqp_host),
            loop=self.loop
        )

        async with self.connection:
            self.channel = await self.connection.channel()

            queue = await self.channel.declare_queue(
                self._service.name,
                auto_delete=False
            )
            async with queue.iterator() as queue_iter:
                async for message in queue_iter:
                    request_body = json.loads(message.body)
                    if request_body.get('message_type') != 'request':
                        print('Handler got and ignore response')
                        message.reject(requeue=True)
                        continue
                    async with message.process():
                        await self._on_amqp_message(msg=message)

    async def stop(self):
        await self.channel.close()
