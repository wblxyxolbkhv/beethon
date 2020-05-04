from typing import List, Optional

from example.models.rate import Rate


class RatesRepository:
    def __init__(self):
        self.rates: List[Rate] = []

    def get_rate(self, film_id) -> Optional[Rate]:
        filtered = list(filter(lambda r: r.film_id == film_id, self.rates))
        if len(filtered) > 0:
            return filtered[0]
        return None

    def add_rate(self, rate):
        self.rates.append(rate)

    def update_rate(self, rate):
        self.rates = list(
            filter(lambda r: r.film_id == rate.film_id, self.rates)
        )
        self.rates.append(rate)
