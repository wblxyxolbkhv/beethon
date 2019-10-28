import http
import json
from typing import Any, Optional, Tuple


class Request:

    def __init__(self, method_name: str, args: Tuple[Any, ...], kwargs: dict):
        self.method_name = method_name
        self.args = args
        self.kwargs = kwargs
        self.message_type = 'request'

    @classmethod
    def parse(cls, json_request: str) -> 'Request':
        request_dict = json.loads(json_request)
        if 'method_name' not in request_dict:
            raise ValueError('Bad request: no method_name field')
        return Request(
            method_name=request_dict['method_name'],
            args=request_dict.get('args', []),
            kwargs=request_dict.get('kwargs', {})
        )

    def serialize(self):
        return json.dumps(self.__dict__)


class Response:

    def __init__(self,
                 result: Optional[Any],
                 status: int = http.HTTPStatus.OK,
                 exception: Optional[Exception] = None):
        self.result = result
        self.status = status
        self.exception = exception
        self.message_type = 'response'

    @property
    def success(self):
        return self.status == http.HTTPStatus.OK

    def serialize(self):

        response_dict = {
            'result': getattr(self.result, '__dict__', None),
            'status': self.status,
            'message_type': self.message_type
        }
        if self.exception is not None:
            exc_dict = {
                'class': str(type(self.exception)),
                'message': str(self.exception)
            }
            response_dict['exception'] = exc_dict

        return json.dumps(response_dict)

    @classmethod
    def parse(cls, json_response: str) -> 'Response':
        response_dict = json.loads(json_response)

        exc_info = response_dict.get('exception', None)
        exception = None
        if exc_info is not None:
            # TODO: make real exception
            exception = Exception(exc_info.get('message'))

        response = Response(
            result=response_dict['result'],
            status=response_dict['status'],
            exception=exception
        )
        return response
