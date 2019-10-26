from typing import List

from beethon.client.dummy import DummyClient
from beethon.handlers.dummy import DummyHandler
from beethon.management.decorators import register
from beethon.services.base import Service
from example.models.film import Film
from example.repositories.films_repository import FilmsRepository


@register(with_handler=DummyHandler)
class FilmsService(Service):

    name = 'FilmsService'

    def __init__(self):
        self.repository = FilmsRepository()

    def get_all_films(self) -> List[Film]:
        return self.repository.get_all_films()


class FilmsServiceInterface:

    def get_all_films(self):
        client = DummyClient(service_name='FilmsService')
        return client.call(method_name='get_all_films')
