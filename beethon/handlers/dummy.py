import asyncio

from beethon.handlers.base import Handler
from beethon.messages.base import Request
from beethon.services.base import Service


class DummyHandler(Handler):
    """
    This handler only available in same project, without publishing
    """

    def __init__(self, service: Service):
        super().__init__(service)
        self.__stop_signal_received = False

    async def run(self):
        while not self.__stop_signal_received:
            await asyncio.sleep(0.5)

    async def stop(self):
        self.__stop_signal_received = True

    async def send_request(self, request: Request):
        return await self._on_new_request(request)
