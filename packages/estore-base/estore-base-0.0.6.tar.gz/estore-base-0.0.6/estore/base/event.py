import uuid
import typing
import datetime
import functools

def map_dict(callback, data):
    return dict(map(functools.partial(lambda y, x: (x[0], y(x[1])), callback), data.items()))

class Event:
    """\"Immutable\" Event class

    """
    __slots__ = ("__name", "__stream", "__version", "__data", "__headers", "__created")
    def __init__(self, name:str, stream:uuid.UUID, version:int, data:dict, headers:dict, created:datetime.datetime=datetime.datetime.now()):
        self.__name = name
        self.__stream = stream
        self.__version = version
        self.__data = data
        self.__headers = headers
        self.__created = created

    def __iter__(self):
        return iter(self.__data.items())

    @property
    def name(self):
        return self.__name

    @property
    def stream(self):
        return self.__stream

    @property
    def version(self):
        return self.__version

    @property
    def data(self):
        return self.__data.copy()

    @property
    def headers(self):
        return self.__headers.copy()

    @property
    def created(self):
        return self.__created

    def __repr__(self):
        return f"Event (name: {self.name}, stream: {self.stream}, version: {self.version}, data, headers, created: {self.created})"
