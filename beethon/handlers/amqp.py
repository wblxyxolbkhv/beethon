import json
import os
from typing import Tuple

from amqp import Channel, Connection, Message    # type: ignore

from beethon.handlers.base import Handler
from beethon.messages.base import Request


class AMQPHandler(Handler):

    def __init__(self, service, **kwargs):
        super().__init__(service)
        amqp_host, amqp_user, amqp_pass = self._get_settings()
        self.connection = Connection(host=amqp_host,
                                     userid=amqp_user,
                                     password=amqp_pass)
        self.channel = Channel(self.connection)

    def _get_settings(self) -> Tuple[str, str, str]:
        host = os.environ.get('AMQP_HOST', 'localhost:5672')
        user = os.environ.get('AMQP_USER', 'guest')
        password = os.environ.get('AMQP_PASSWORD', 'guest')

        return host, user, password

    def _on_amqp_message(self, msg: Message):
        body_dict = json.loads(msg.body)
        # accept message for execution
        self.channel.basic_ack(msg.delivery_tag)

        method_name = body_dict['method_name']
        args = body_dict['args']
        kwargs = body_dict['kwargs']

        request = Request(method_name=method_name,
                          args=args,
                          kwargs=kwargs)
        response = self._on_new_request(request)
        serialized_response = response.serialize()
        response_message = Message(body=serialized_response,
                                   correlation_id=msg.properties['correlation_id'])
        self.channel.basic_publish(msg=response_message)

    def run(self):
        self.connection.connect()
        self.channel.open()
        self.channel.queue_declare(queue=self._service.name)
        self.channel.basic_consume(queue=self._service.name,
                                   callback=self._on_amqp_message)

    def stop(self):
        self.channel.close()
