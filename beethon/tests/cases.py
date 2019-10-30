import beethon


class BaseBeethonTestCase:

    def setup(self) -> None:
        beethon.run_async()

    def teardown(self) -> None:
        beethon.stop()
