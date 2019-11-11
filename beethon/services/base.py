from typing import Dict, Any, Tuple, Callable

from beethon.utils.singleton import MetaSingleton


class Service(metaclass=MetaSingleton):
    name = ''

    _methods_attrs: Dict[str:Dict[str:Any]] = {}

    def change_url(self, method_name, new_url):
        method_dict = self._methods_attrs.get(method_name, {})
        method_dict['url'] = new_url

    def specify_http_method(self, method_name, http_method):

        methods = ['GET', 'POST', 'PUT', 'DELETE',
                   'PATCH', 'HEAD', 'OPTIONS', '*']

        if http_method not in methods:
            raise ValueError('Wrong http method. '
                             'Method must be one of {}'.format(', '.join(methods)))

        method_dict = self._methods_attrs.get(method_name, {})
        method_dict['http_method'] = http_method

    def __iter__(self) -> Tuple[Callable, Dict[str:Any]]:
        """
        Returns all public methods with attrs
        :return: (method, attrs dict)
        """
        for attr in dir(self):
            if attr.startswith(('__', '_')) or attr == 'change_url':
                continue
            method = getattr(self, attr)
            if callable(method):
                attrs = self._methods_attrs.get(attr, {})
                yield method, attrs
