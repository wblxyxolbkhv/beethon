import http
from abc import ABC, abstractmethod
from threading import Thread
from typing import Optional

from beethon.messages.base import Request, Response
from beethon.services.base import Service


class Handler(ABC):

    def __init__(self, service: Service):
        self.__service = service

    @abstractmethod
    def run(self):
        raise NotImplementedError('run() method of handler must be implemented in children')

    @abstractmethod
    def stop(self):
        raise NotImplementedError('stop() method of handler must be implemented in children')

    def _on_new_request(self, request: Request) -> Response:
        result = None
        status = http.HTTPStatus.OK
        exc: Optional[Exception] = None

        try:
            service_method = getattr(self.__service, request.method_name, None)
            result = service_method(*request.args, **request.kwargs)
        except AttributeError as e:
            exc = e
            status = http.HTTPStatus.BAD_REQUEST
        except Exception as e:
            exc = e
            status = http.HTTPStatus.INTERNAL_SERVER_ERROR

        return Response(result=result, status=status, exception=exc)

    def get_service(self) -> Service:
        return self.__service


class HandlerRunThread(Thread):

    def __init__(self, handler: Handler):
        super().__init__(target=handler.run)
        self.handler = handler

    def stop(self):
        self.handler.stop()
