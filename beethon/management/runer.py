import asyncio
from asyncio import Future, Task
from concurrent.futures.thread import ThreadPoolExecutor
from threading import Thread
from typing import List, Optional

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

    def run(self):
        loop = asyncio.get_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self._run())

    def run_async(self):
        asyncio.ensure_future(self._run())

    async def _run(self):
        self._run_tasks = []
        for handler in self.config:
            self._run_tasks.append(asyncio.create_task(handler.run()))

        await asyncio.gather(*self._run_tasks)

    def stop(self):
        for task in self._run_tasks:
            task.cancel()
