import asyncio
import json
import os
import uuid
from datetime import timedelta
from typing import Optional, Any, Tuple

import aio_pika
from aio_pika import Message, Queue

from beethon.client.base import Client
from beethon.exceptions.response_exceptions import CantConnect
from beethon.messages.base import Request, Response


class AMQPClient(Client):
    """
    Async RPC client with AMQP transport.

    By default use 2 queues: for requests and for responses.

    Usage example:

    client = AMQPClient(service_name)
    result = await client.call('method', foo='bar')
    client.stop()

    or

    async with AMQPClient(service_name) as client:
        result = await client.call('method', foo='bar')

    """

    def __init__(
        self,
        service_name: str,
        timeout: int = 10,
        loop=None,
        amqp_host: str = None,
        amqp_user: str = None,
        amqp_password: str = None,
    ):

        super().__init__(service_name=service_name)
        self.timeout = timeout

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

        if loop is None:
            self.loop = asyncio.get_event_loop()
        else:
            self.loop = loop

        self.request_queue: Optional[Queue] = None
        self.response_queue: Optional[Queue] = None

    def _get_settings(self) -> Tuple[str, str, str]:
        host = os.environ.get("BEETHON_AMQP_HOST", "localhost:5672")
        user = os.environ.get("BEETHON_AMQP_USER", "guest")
        password = os.environ.get("BEETHON_AMQP_PASSWORD", "guest")

        return host, user, password

    def _get_request_queue_name(self):
        return "{}-requests".format(self.service_name)

    def _get_response_queue_name(self):
        return "{}-responses".format(self.service_name)

    async def _connect(self):
        self.connection = await aio_pika.connect_robust(self.amqp_url, loop=self.loop)
        await self.connection.connect(timeout=self.timeout)
        self.channel = await self.connection.channel()
        self.request_queue = await self.channel.declare_queue(
            self._get_request_queue_name(), auto_delete=False
        )
        self.response_queue = await self.channel.declare_queue(
            self._get_response_queue_name(), auto_delete=False
        )

    async def call(self, method_name: str, **kwargs) -> Optional[Any]:
        """
        Make async call of remote service method via AMQP
        :param method_name: method name of service
        :param kwargs: keyword arguments of method
        :return: result of call
        """
        return await asyncio.wait_for(
            self._call(method_name, **kwargs), timeout=self.timeout
        )

    async def _call(self, method_name: str, **kwargs) -> Optional[Any]:

        if self.connection is None or not await self.connection.ready():
            await self._connect()

        if self.channel is None or self.response_queue is None:
            raise CantConnect()

        request = Request(method_name=method_name, kwargs=kwargs)
        correlation_id = uuid.uuid4().hex
        message = Message(
            body=request.serialize().encode(),
            correlation_id=correlation_id,
            expiration=timedelta(seconds=self.timeout),
        )
        await self.channel.default_exchange.publish(
            message=message, routing_key=self._get_request_queue_name()
        )

        async with self.response_queue.iterator() as queue_iter:
            async for msg in queue_iter:
                response_dict = json.loads(msg.body)
                if (
                    msg.correlation_id != correlation_id
                    or response_dict.get("message_type") != "response"
                ):
                    print("Got and ignored message")
                    msg.reject(requeue=True)
                    continue
                async with msg.process():
                    exc = None
                    if response_dict.get("exception"):
                        exc = Exception("")
                    response = Response(
                        result=response_dict["result"],
                        status=int(response_dict["status"]),
                        exception=exc,
                    )
                    break

            return self.process_response(response)

    async def stop(self):
        if self.connection and await self.connection.ready():
            await self.connection.close()

    async def __aenter__(self):
        await self._connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.stop()
