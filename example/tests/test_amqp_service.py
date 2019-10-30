
from beethon.client.amqp import AMQPClient
from beethon.tests.cases import BaseBeethonTestCase

import pytest


# class RatesServiceTestCase(TestCase):
#
#     def setUp(self):
#         from example.services.rates import RatesService     # noqa
#         super().setUp()
#
#     async def test_rate_film(self):
#         sleep(5)
#         client = AMQPClient(service_name='RatesService')
#         await client.call('rate_film', film_id=1, rating=5)
#         rate_dict = await client.call('get_rate', film_id=1)
#         self.assertEqual(rate_dict['film_id'], 1)
#         self.assertEqual(rate_dict['rate'], 5)

class TestAMQPService(BaseBeethonTestCase):

    def setup(self) -> None:
        from example.services.rates import RatesService     # noqa
        super().setup()

    @pytest.mark.asyncio
    async def test_rate_film(self):
        client = AMQPClient(service_name='RatesService')
        await client.call('rate_film', film_id=1, rating=5)
        rate_dict = await client.call('get_rate', film_id=1)
        assert rate_dict['film_id'] == 1
        assert rate_dict['rate'] == 5
