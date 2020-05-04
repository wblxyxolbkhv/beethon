from abc import ABC, abstractmethod
from typing import Optional, Any

from beethon.messages.base import Response


class Client(ABC):
    def __init__(self, service_name: str):
        self.service_name = service_name

    @abstractmethod
    def call(self, method_name: str, *args, **kwargs) -> Optional[Any]:
        raise NotImplementedError("call() method must be "
                                  "implement in children!")

    def process_response(self, response: Response) -> Optional[Any]:
        if response.exception is not None:
            raise response.exception
        if not response.success:
            # TODO: raise real exception
            raise Exception()
        return response.result
