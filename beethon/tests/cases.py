from threading import Thread
from unittest import TestCase

import beethon


class BeethonRunThread(Thread):

    def run(self) -> None:
        beethon.run()

    def stop(self) -> None:
        beethon.stop()


class BaseBeethonTestCase(TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.thread = BeethonRunThread()
        self.thread.start()

    def tearDown(self) -> None:
        super().tearDown()
        self.thread.stop()
