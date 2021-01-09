from multiprocessing import connection
from typing import Any, Dict, Callable, Generator, Tuple, Union

from lib.terminal_ui import Element

TextDisplay = Any
CompilerCommand = Union[str, Callable[[], str]]
PipeConnection = connection.Connection
PipeMessage = Dict[str, str]
TextDisplayable = Union[str, Element]
TextDisplayableMessage = Union[TextDisplayable, Tuple[TextDisplayable, int]]
TextDisplayableHandler = Generator[TextDisplayableMessage, None, None]
