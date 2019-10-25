from beethon.tests.cases import BaseBeethonTestCase


class FilmServiceTestCase(BaseBeethonTestCase):

    def test_get_all_films(self):
        from example.services.films import FilmsServiceInterface
        interface = FilmsServiceInterface()
        films = interface.get_all_films()
        self.assertEqual(len(films), 3)
