from typing import List

from beethon.handlers.dummy import DummyHandler
from beethon.management.decorators import register
from beethon.services.base import Service
from example.models.film import Film
from example.repositories.films_repository import FilmsRepository


@register(with_handler=DummyHandler)
class FilmsService(Service):

    name = "FilmsService"

    def __init__(self):
        self.repository = FilmsRepository()

    async def get_all_films(self) -> List[Film]:
        return self.repository.get_all_films()

    async def raising_method(self):
        raise ValueError("oops")
