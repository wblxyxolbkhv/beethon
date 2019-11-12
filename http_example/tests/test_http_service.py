import asyncio

from beethon.client.http import HTTPClient
from beethon.tests.cases import BaseBeethonTestCase


class TestHTTPService(BaseBeethonTestCase):

    def setup(self):
        from http_example.services.comments import CommentsService     # noqa
        super().setup()

    def test_get_comment(self):
        async def _test_get_comment():
            async with HTTPClient(
                    service_name='comments',
                    host='127.0.0.1',
                    port=9090) as client:
                result = client.call('get', comment_id=1)
                assert result['id'] == 1
                assert result['text'] != ''

        loop = asyncio.get_event_loop()
        loop.run_until_complete(_test_get_comment())
