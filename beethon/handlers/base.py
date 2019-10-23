import http
from abc import ABC, abstractmethod
from typing import Dict, Hashable

from beethon.messages.base import Request, Response
from beethon.services.base import Service


class Handler(ABC):

    def __init__(self, service: Service):
        self.__service = service

    @abstractmethod
    def run(self):
        raise NotImplementedError('run() method of handler must be implemented in children')

    def __on_new_request(self, request: Request) -> Response:
        result = None
        status = http.HTTPStatus.OK
        exc = None

        try:
            service_method = getattr(self.__service, request.method_name, None)
            result = service_method(*request.args, **request.kwargs)
        except AttributeError as e:
            exc = e
            status = http.HTTPStatus.BAD_REQUEST
        except Exception as e:
            status = http.HTTPStatus.INTERNAL_SERVER_ERROR
            exc = e

        return Response(result=result, status=status, exception=exc)
