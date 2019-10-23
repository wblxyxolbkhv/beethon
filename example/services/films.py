from typing import List

from beethon.services.base import Service
from example.models.film import Film
from example.repositories.films_repository import FilmsRepository


class FilmsService(Service):

    def __init__(self):
        self.repository = FilmsRepository()

    def get_all_films(self) -> List[Film]:
        return self.repository.get_all_films()