from typing import Type

from beethon.management.config import BeethonConfig
from beethon.services.base import Service


def register(with_handler: Type = None, **kwargs):
    """
    Register service for beethon handling
    :param with_handler: handler class
    :param kwargs: keyword arguments for initializing handler instance
    :return:
    """

    def _service_wrapper(service_class):
        BeethonConfig().register(service_class, handler_class=with_handler, **kwargs)
        return service_class

    return _service_wrapper


def route(method: str = None, path: str = None):
    """
    Specify http route for service method
    :param method: http method (GET, POST, ..)
    :param path:
    :return:
    """

    def _route_wrapper(service_method):
        service: Service = service_method.__self__
        if method is not None:
            service.specify_http_method(service_method.__name__, method)
        if path is not None:
            service.change_url(service_method.__name__, path)
        return service_method

    return _route_wrapper
