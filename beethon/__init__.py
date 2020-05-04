from beethon.management.runer import AsyncBeethonRunner

runner = AsyncBeethonRunner()


async def run():
    await runner.run()


def stop():
    runner.stop()
