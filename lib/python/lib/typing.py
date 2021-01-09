from multiprocessing import connection
from typing import Dict

PipeConnection = connection.Connection
PipeMessage = Dict[str, str]
