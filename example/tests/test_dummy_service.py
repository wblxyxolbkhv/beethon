import asyncio

import pytest

from beethon.client.dummy import DummyClient
from beethon.tests.cases import BaseBeethonTestCase


@pytest.mark.unit
class TestDummyService(BaseBeethonTestCase):
    def setup(self) -> None:
        from example.services.films import FilmsService  # noqa

        super().setup()

    async def coro_get_all_films(self):
        client = DummyClient(service_name="FilmsService")
        films = await client.call(method_name="get_all_films")
        assert len(films) == 3

    def test_get_all_films(self):
        asyncio.get_event_loop().run_until_complete(self.coro_get_all_films())

    async def coro_raise(self):
        client = DummyClient(service_name="FilmsService")
        await client.call(method_name="raising_method")

    def test_raise(self):
        with pytest.raises(Exception):
            asyncio.get_event_loop().run_until_complete(self.coro_raise())
