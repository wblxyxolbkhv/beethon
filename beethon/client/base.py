from abc import ABC, abstractmethod
from typing import Optional, Any

from beethon.messages.base import Response


class Client(ABC):

    @abstractmethod
    def call(self, service_name: str, method_name: str, *args, **kwargs) -> Optional[Any]:
        raise NotImplementedError('call() method must be implement in children!')

    def process_response(self, response: Response) -> Optional[Any]:
        if response.exception is not None:
            raise response.exception
        return response.result
