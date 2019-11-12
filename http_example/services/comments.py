from beethon.handlers.http import HTTPHandler
from beethon.management.decorators import register, route
from beethon.services.base import Service


@register(with_handler=HTTPHandler, base_url='comments', port=9090)
class CommentsService(Service):

    @route(path='/add', method='POST')
    async def add_comment(self, film_id: int, comment: str):
        return 'ok'

    @route(path='/get', method='GET')
    async def get_comment(self, comment_id: int):
        return {
            'id': comment_id,
            'text': 'This is astonishing!'
        }
