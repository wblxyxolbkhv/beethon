from beethon.management.runer import BeethonRunner, AsyncBeethonRunner

# runner = BeethonRunner()
runner = AsyncBeethonRunner()


def run():
    runner.run()


def run_async():
    runner.run_async()


def stop():
    runner.stop()
