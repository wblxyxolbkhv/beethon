from beethon.handlers.amqp import AMQPHandler
from beethon.management.decorators import register
from beethon.services.base import Service
from example.models.rate import Rate
from example.repositories.rates_repository import RatesRepository


@register(with_handler=AMQPHandler)
class RatesService(Service):

    name = 'RatesService'

    def __init__(self):
        self.repo = RatesRepository()

    async def rate_film(self, film_id: int, rating: int):
        rate = self.repo.get_rate(film_id=film_id)
        new_rate = Rate(film_id=film_id, rate=rating)
        if rate is None:
            self.repo.add_rate(new_rate)
        else:
            self.repo.update_rate(new_rate)

    async def get_rate(self, film_id: int) -> Rate:
        return self.repo.get_rate(film_id)
