import asyncio

import pytest

import beethon


class BaseBeethonTestCase:
    def setup(self):
        asyncio.ensure_future(beethon.run())

    def teardown(self):
        beethon.stop()
