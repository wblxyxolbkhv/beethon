import asyncio
from asyncio import Future
from contextlib import suppress
from typing import List

from beethon.management.config import BeethonConfig


class AsyncBeethonRunner:

    def __init__(self):
        self.config = BeethonConfig()
        self._run_tasks: List[Future] = []

    async def run(self):
        await self._run()

    async def _run(self):
        print('Run beethon..')
        self._run_tasks = []
        for handler in self.config:
            self._run_tasks.append(asyncio.create_task(handler.run()))

        await asyncio.gather(*self._run_tasks)

    def stop(self):
        print('Stop beethon..')
        for task in self._run_tasks:
            task.cancel()
        # loop = asyncio.get_event_loop()
        # with suppress(asyncio.CancelledError):
        #     loop.run_until_complete(asyncio.gather(*self._run_tasks))
