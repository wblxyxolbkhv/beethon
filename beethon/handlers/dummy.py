from time import sleep

from beethon.handlers.base import Handler


class DummyHandler(Handler):
    """
    This handler only available in same project, without publishing
    """
    def run(self):
        while True:
            sleep(1)
