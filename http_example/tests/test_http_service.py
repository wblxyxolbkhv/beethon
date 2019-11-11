import asyncio

from beethon.client.amqp import AMQPClient
from beethon.tests.cases import BaseBeethonTestCase


class TestHTTPService(BaseBeethonTestCase):

    def setup(self):
        from http_example.services.comments import CommentsService     # noqa
        super().setup()

    def teardown(self):
        super().teardown()

    async def coro_rate_film_context_manager(self):
        assert False

    def test_rate_film_context_manager(self):
        event_loop = asyncio.get_event_loop()
        event_loop.run_until_complete(self.coro_rate_film_context_manager())
