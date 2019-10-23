from threading import Thread
from typing import List

import beethon
from beethon.management.config import BeethonConfig


class BeethonRunner:

    def __init__(self):
        self.config = BeethonConfig()

    def run(self):
        # TODO: think about async
        threads = []    # type: List[Thread]

        for handler in self.config:
            thread = Thread(target=handler.run)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()
