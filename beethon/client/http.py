from typing import Any, Optional

from beethon.client.base import Client


class HTTPClient(Client):

    async def call(self, method_name: str, *args, **kwargs) -> Optional[Any]:
        pass
