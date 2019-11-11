from beethon.handlers.http import HTTPHandler
from beethon.management.decorators import register, route
from beethon.services.base import Service


@register(with_handler=HTTPHandler, base_url='comments')
class CommentsService(Service):

    @route(path='/add', method='GET')
    async def add_comment(self, film_id: int, comment: str):
        return 0
