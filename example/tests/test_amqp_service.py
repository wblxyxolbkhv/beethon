import asyncio

from beethon.client.amqp import AMQPClient
from beethon.tests.cases import BaseBeethonTestCase


class TestAMQPService(BaseBeethonTestCase):

    def setup(self):
        from example.services.rates import RatesService     # noqa
        super().setup()

    def teardown(self):
        super().teardown()

    async def coro_rate_film_context_manager(self):
        async with AMQPClient(service_name='RatesService') as client:
            await client.call('rate_film', film_id=1, rating=5)
            rate_dict = await client.call('get_rate', film_id=1)
        assert rate_dict['film_id'] == 1
        assert rate_dict['rate'] == 5

    def test_rate_film_context_manager(self):
        event_loop = asyncio.get_event_loop()
        event_loop.run_until_complete(self.coro_rate_film_context_manager())

    def test_rate_film(self):
        event_loop = asyncio.get_event_loop()
        client = AMQPClient(service_name='RatesService', loop=event_loop)
        event_loop.run_until_complete(client.call('rate_film', film_id=1, rating=5))
        rate_dict = event_loop.run_until_complete(client.call('get_rate', film_id=1))
        assert rate_dict['film_id'] == 1
        assert rate_dict['rate'] == 5
