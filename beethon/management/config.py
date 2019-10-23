from typing import List, Type, Optional

from beethon.handlers.base import Handler
from beethon.handlers.dummy import DummyHandler
from beethon.services.base import Service


class BeethonConfig:

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(BeethonConfig, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.__handlers = []    # type: List[Handler]
        self.default_handler_class = DummyHandler

    def __iter__(self):
        return self.__handlers.__iter__()

    def register(self, service_class: Type, handler_class: Optional[Type]):
        if handler_class is None:
            handler_class = self.default_handler_class

        if not issubclass(service_class, Service):
            raise TypeError('You can register only Service subclasses!')
        if not issubclass(handler_class, Handler):
            raise TypeError('You can register only on Handler subclasses!')

        handler = handler_class(service=service_class())

        self.__handlers.append(handler)
