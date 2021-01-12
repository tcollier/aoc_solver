from multiprocessing import connection
from typing import Dict, Generator, Tuple, Union


class Stringable:
    def __repr__(self):
        raise NotImplementedError(f"{type(self).__name__} must implement __repr__()")


PipeConnection = connection.Connection
PipeMessage = Dict[str, str]
Priority = int
TextDisplayable = Union[str, Stringable]
TextDisplayableMessage = Union[TextDisplayable, Tuple[TextDisplayable, Priority]]
TextDisplayableHandler = Generator[TextDisplayableMessage, None, None]
