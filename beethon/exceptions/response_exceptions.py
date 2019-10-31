

class ThereIsNoSuchService(Exception):
    pass


class CantConnect(ConnectionError):
    pass


class Disconnect(ConnectionError):
    pass


class HttpLikeException(Exception):
    pass
