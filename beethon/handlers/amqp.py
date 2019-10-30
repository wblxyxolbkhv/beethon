import asyncio
import json
import os
from typing import Tuple, Optional

import aio_pika
from aio_pika import IncomingMessage, Message, Queue

from beethon.handlers.base import Handler
from beethon.messages.base import Request
from beethon.services.base import Service


class AMQPHandler(Handler):
    """
    Handler for services with AMQP transport

    By default use 2 queues: for requests and for responses.
    """

    def __init__(self,
                 service: Service,
                 amqp_host: str = None,
                 amqp_user: str = None,
                 amqp_password: str = None):
        super().__init__(service)

        host, user, password = self._get_settings()
        if amqp_host is None:
            amqp_host = host
        if amqp_user is None:
            amqp_user = user
        if amqp_password is None:
            amqp_password = password

        self.amqp_url = "amqp://{}:{}@{}".format(amqp_user, amqp_password, amqp_host)

        self.connection: Optional[aio_pika.Connection] = None
        self.channel: Optional[aio_pika.Channel] = None
        self.loop = asyncio.get_event_loop()

        self.request_queue: Optional[Queue] = None
        self.response_queue: Optional[Queue] = None

    def _get_settings(self) -> Tuple[str, str, str]:
        host = os.environ.get('BEETHON_AMQP_HOST', 'localhost:5672')
        user = os.environ.get('BEETHON_AMQP_USER', 'guest')
        password = os.environ.get('BEETHON_AMQP_PASSWORD', 'guest')

        return host, user, password

    def _get_request_queue_name(self):
        return '{}-requests'.format(self._service.name)

    def _get_response_queue_name(self):
        return '{}-responses'.format(self._service.name)

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
        await self.channel.default_exchange.publish(message=message, routing_key=self._get_response_queue_name())

    async def run(self):
        self.connection = await aio_pika.connect_robust(
            self.amqp_url,
            loop=self.loop
        )

        async with self.connection:
            self.channel = await self.connection.channel()

            self.request_queue = await self.channel.declare_queue(
                self._get_request_queue_name(),
                auto_delete=False
            )
            self.response_queue = await self.channel.declare_queue(
                self._get_response_queue_name(),
                auto_delete=False
            )
            async with self.request_queue.iterator() as queue_iter:
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
