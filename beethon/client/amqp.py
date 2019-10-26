import json
import os
import uuid
from typing import Optional, Any, Tuple, Dict

import amqp     # type: ignore
from amqp import Connection, Channel, Message

from beethon.client.base import Client
from beethon.exceptions.response_exceptions import ThereIsNoSuchService
from beethon.messages.base import Request, Response


class AMQPClient(Client):

    def __init__(self, service_name: str):
        super().__init__(service_name=service_name)
        amqp_host, amqp_user, amqp_pass = self._get_settings()
        self.connection = Connection(host=amqp_host,
                                     userid=amqp_user,
                                     password=amqp_pass)
        self.channel = Channel(self.connection)

        self._responses: Dict[str, Response] = {}

    def _get_settings(self) -> Tuple[str, str, str]:
        host = os.environ.get('AMQP_HOST', 'localhost:5672')
        user = os.environ.get('AMQP_USER', 'guest')
        password = os.environ.get('AMQP_PASSWORD', 'guest')

        return host, user, password

    def call(self, method_name: str, *args, **kwargs) -> Optional[Any]:
        request = Request(method_name=method_name, args=args, kwargs=kwargs)
        correlation_id = uuid.uuid4().hex
        message = Message(body=request.serialize(), correlation_id=correlation_id)
        self.channel.open()
        self.channel.basic_publish(msg=message)

        def wait_response(msg: Message):
            if msg.properties['correlation_id'] == correlation_id:
                response_dict = json.loads(msg.body)
                exc = None
                if response_dict.get('exception'):
                    exc = Exception('')
                self._responses[correlation_id] = Response(
                    result=response_dict['result'],
                    status=int(response_dict['status']),
                    exception=exc
                )
                self.channel.close()
        try:
            self.channel.basic_consume(queue=self.service_name, callback=wait_response)
        except amqp.exceptions.NotFound:
            raise ThereIsNoSuchService()
        return self.process_response(self._responses.pop(correlation_id))
