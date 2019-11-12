from typing import Any, Optional

import beethon
from beethon.client.base import Client
from beethon.exceptions.response_exceptions import ThereIsNoSuchService
from beethon.handlers.dummy import DummyHandler
from beethon.messages.base import Request


class DummyClient(Client):
    async def call(self, method_name: str, **kwargs) -> Optional[Any]:

        for handler in beethon.runner.config:
            if (
                type(handler) == DummyHandler
                and handler.get_service().name == self.service_name
            ):
                response = await handler.send_request(
                    Request(method_name=method_name, kwargs=kwargs)
                )
                return self.process_response(response)

        raise ThereIsNoSuchService()
