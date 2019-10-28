import asyncio
from asyncio import Future
from concurrent.futures.thread import ThreadPoolExecutor
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


class AsyncBeethonRunner:

    def __init__(self):
        self.config = BeethonConfig()
        self._run_tasks: List[Future] = []

        self.run_future = None

    def run(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._run())
        loop.close()

    def run_async(self):
        executor = ThreadPoolExecutor(max_workers=2)
        loop = asyncio.get_event_loop()
        loop.run_in_executor(executor, self.run)

    async def _run(self):
        self._run_tasks = []
        for handler in self.config:
            self._run_tasks.append(handler.run())

        await asyncio.gather(*self._run_tasks)

    def stop(self):
        for task in self._run_tasks:
            task.cancel()



