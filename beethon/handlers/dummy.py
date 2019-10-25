from time import sleep

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

    def run(self):
        while not self.__stop_signal_received:
            sleep(0.5)

    def stop(self):
        self.__stop_signal_received = True

    def send_request(self, request: Request):
        return self._on_new_request(request)
