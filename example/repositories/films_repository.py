from typing import List

from example.models.film import Film


class FilmsRepository:

    def get_all_films(self) -> List[Film]:
        return [
            Film(name='The Shawshank Redemption',
                 description='Fear can hold you prisoner. Hope can set you free.',
                 year=1994),
            Film(name='The Terminator',
                 description='Your future in his hands.',
                 year=1984),
            Film(name='Rush Hour',
                 description='The fastest hands in the East meet the biggest mouth in the West.',
                 year=1998),
        ]