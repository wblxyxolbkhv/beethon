from typing import List

from beethon.handlers.base import HandlerRunThread
from beethon.management.config import BeethonConfig


class BeethonRunner:

    def __init__(self):
        self.config = BeethonConfig()
        self.threads = []   # type: List[HandlerRunThread]

    def run(self):
        # TODO: think about async

        for handler in self.config:
            thread = HandlerRunThread(handler)
            thread.start()
            self.threads.append(thread)

        for thread in self.threads:
            thread.join()

    def stop(self):
        for thread in self.threads:
            thread.stop()
