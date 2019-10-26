from beethon.client.amqp import AMQPClient
from beethon.tests.cases import BaseBeethonTestCase


class RatesServiceTestCase(BaseBeethonTestCase):

    def setUp(self):
        from example.services.rates import RatesService     # noqa
        super().setUp()

    def test_rate_film(self):
        client = AMQPClient(service_name='RatesService')
        client.call('rate_film', film_id=1, rating=5)
        rate_dict = client.call('get_rate', film_id=1)
        self.assertEqual(rate_dict['film_id'], 1)
        self.assertEqual(rate_dict['rate'], 5)
