![logo](https://i.ibb.co/PzjhcXG/beethon.png)
# Beethon
![travis badge](https://travis-ci.org/wblxyxolbkhv/beethon.svg?branch=master)
[![Python 3](https://pyup.io/repos/github/wblxyxolbkhv/beethon/python-3-shield.svg)](https://pyup.io/repos/github/wblxyxolbkhv/beethon/)
[![Coverage Status](https://coveralls.io/repos/github/wblxyxolbkhv/beethon/badge.svg?branch=master)](https://coveralls.io/github/wblxyxolbkhv/beethon?branch=master)
[![Updates](https://pyup.io/repos/github/wblxyxolbkhv/beethon/shield.svg)](https://pyup.io/repos/github/wblxyxolbkhv/beethon/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Simple async python-based microservice framework

## Example

Service example:

```python
import asyncio

import beethon
from beethon.handlers.amqp import AMQPHandler
from beethon.management.decorators import register
from beethon.services.base import Service


@register(with_handler=AMQPHandler)
class SomeService(Service):

    name = "some-service"
    
    async def do_something(self, foo, bar=None):
        # ...
        await something_else()
        # ...
        return result

if __name__ = '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(beethon.run())

```

Client example:
```python

from beethon.clients.amqp import AMQPClient

async def main():
    async with AMQPClient(service_name='some-service') as client:
        result = await client.call('do_something', foo="foo", bar="bar")

if __name__ = '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

```

## In the plans 

* HTTP handler and client
* Integration with Netfix Stack
* OpenAPI Scheme generation


## Contributing

Contributions are always welcome! Just fork and help the project.

## Feedback

For feedback write to alexey.nikitenko1927@gmail.com

## License

[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

- **[MIT license](http://opensource.org/licenses/mit-license.php)**
