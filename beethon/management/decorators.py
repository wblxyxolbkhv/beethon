from typing import Type

from beethon.management.config import BeethonConfig


def register(with_handler: Type=None):

    def _service_wrapper(service_class):
        BeethonConfig().register(service_class, handler_class=with_handler)

    return _service_wrapper
