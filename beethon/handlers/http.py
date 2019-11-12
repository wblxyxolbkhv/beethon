from typing import Optional

import aiohttp
from aiohttp import web
from aiohttp import web_request
from aiohttp.web_response import StreamResponse
from aiohttp.web_runner import AppRunner

import beethon
from beethon.handlers.base import Handler
from beethon.messages.base import Request
from beethon.services.base import Service


class HTTPHandler(Handler):
    """
    Handler for services with HTTP transport
    """

    def __init__(self,
                 service: Service,
                 base_url: str = '/',
                 port: Optional[int] = None):
        super().__init__(service=service)

        self.runner: Optional[AppRunner] = None

        self.override_port = port

        self.base_url = self._clean_url(base_url)

    def _clean_url(self, url: str) -> str:
        if not url.startswith('/'):
            url = '/' + url

        return url

    def _get_port(self):
        """
        Returns port for handling
        :return:
        """
        if self.override_port is None:
            return beethon.runner.config.default_http_port
        return self.override_port

    def _configure_routes(self, app: web.Application):
        """
        Configure urls for service
        :param app:
        :return:
        """
        for method, attrs in self.get_service():
            # use custom url from decorator or just method name
            url = attrs.get('url') or method.__name__
            url = self._clean_url(url)
            url = self.base_url + url
            http_method = attrs.get('http_method') or '*'
            app.router.add_route(http_method, url, self._http_handler)

    def _get_method_name(self, url: str) -> str:
        """
        Match url to service method name
        :param url:
        :return:
        """

        url = url.lstrip(self.base_url)

        for method, attrs in self.get_service():
            method_url = attrs.get('url')
            if method_url is not None and method_url == url:
                return method.__name__

        url = url.lstrip('/')

        for method, attrs in self.get_service():
            if method.__name__ == url:
                return method.__name__

        raise AttributeError()

    async def _http_handler(self, request: web_request.Request) -> StreamResponse:
        """
        Handle every request for service
        :param request:
        :return:
        """
        handler_func = getattr(self, '_{}'.format(request.method))
        return await handler_func(request)

    async def _GET(self, request: web_request.Request) -> StreamResponse:
        """
        Handle GET requests for service

        By default GET parameters will be kwargs for service method call

        :param request:
        :return:
        """
        kwargs = {}
        kwargs.update(**request.match_info)

        method_name = self._get_method_name(url=request.rel_url.path)

        beethon_request = Request(method_name=method_name,
                                  kwargs=kwargs)
        response = StreamResponse()
        try:
            beethon_reponse = await self._on_new_request(request=beethon_request)
            await response.write(beethon_reponse.serialize().encode())
        except Exception:
            # TODO: make exception more specific
            response.set_status(500)
        return response

    async def _POST(self, request: Request) -> StreamResponse:
        return StreamResponse()

    async def _DELETE(self, request: Request) -> StreamResponse:
        return StreamResponse()

    async def _PUT(self, request: Request) -> StreamResponse:
        return StreamResponse()

    async def _PATCH(self, request: Request) -> StreamResponse:
        return StreamResponse()

    async def _HEAD(self, request: Request) -> StreamResponse:
        return StreamResponse()

    async def _OPTIONS(self, request: Request) -> StreamResponse:
        return StreamResponse()

    async def run(self):
        app = web.Application()
        self.configure_routes(app)
        self.runner = web.AppRunner(app)
        await self.runner.setup()
        site = web.TCPSite(self.runner, '0.0.0.0', self._get_port())
        await site.start()

    async def stop(self):
        await self.runner.cleanup()
