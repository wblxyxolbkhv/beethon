from typing import Any, Optional, Mapping

import aiohttp

from beethon.client.base import Client
from beethon.messages.base import Response


class HTTPClient(Client):

    def __init__(self, service_name: str, host: str, port: int):
        super().__init__(service_name)

        self.host = host
        self.port = port
        self.session: Optional[aiohttp.ClientSession] = None

    def _get_base_url(self) -> str:
        return f'{self.host}:{self.port}/{self.service_name}'

    def _get_full_url(self, method_url: str) -> str:
        return f'{self._get_base_url()}/{method_url}'

    async def call(self, method_name: str, **kwargs) -> Optional[Any]:
        return await self.call_with_method(method_name=method_name, http_method='GET', params=kwargs)

    async def call_with_method(self,
                               method_name: str,
                               http_method: str,
                               params: Mapping[str, str] = None,
                               **kwargs) -> Optional[Any]:

        json = None
        if params is None:
            json = kwargs

        async with self.session.request(
            method=http_method,
            url=self._get_full_url(method_url=method_name),
            params=params,
            json=json
        ) as resp:
            resp_dict = await resp.json()
            response = Response(
                result=resp_dict.get('result'),
                # TODO: which status better, http or internal?
                status=resp.status,
                exception=resp_dict.get('exception')
            )
            return self.process_response(response)

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()