from multiprocessing import connection
from typing import Dict, Iterator, Tuple, Union


class Stringable:
    @property
    def is_error(_self):
        return False

    def __repr__(self):
        raise NotImplementedError(f"{type(self).__name__} must implement __repr__()")


PipeConnection = connection.Connection
PipeMessage = Dict[str, str]
Priority = int
StringableMessage = Union[Stringable, Tuple[Stringable, Priority]]
StringableIterator = Iterator[StringableMessage]
