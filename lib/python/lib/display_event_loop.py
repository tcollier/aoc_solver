from __future__ import annotations
from dataclasses import dataclass, field
from queue import PriorityQueue
from typing import Any, Callable, Dict, Generator

from lib.shell import is_process_running
from lib.solver_event import SolverEvent
from lib.typing import PipeConnection, TextDisplayableMessage


class DisplayEventLoop:
    def __init__(self, display: Any, conn: PipeConnection, refresh_rate: int = 30):
        """
        :param refresh_rate: rate (in frames per second) at which events are process
        and thus the maximum rate the display will be updated.
        """
        self._handler = TextHandler(display)
        self._conn = conn
        self._refresh_rate = refresh_rate

    def __call__(self, parent_pid: int):
        """
        :param parent_pid: Process ID of the parent that spawned the this event loop.
        Keep tabs on it so we can exit if it mysteriously vanishes, e.g. with a SIGKILL
        """
        running = True
        while running:
            if self._conn.poll(1 / self._refresh_rate):
                message = self._conn.recv()
                event = message["event"]
                self._handler.handle(message)
                if event == SolverEvent.TERMINATE:
                    running = False
            if not is_process_running(parent_pid):
                self._handler.handle(
                    {
                        "event": SolverEvent.TERMINATE,
                        "error": "Main process has disappeared!",
                    }
                )
                running = False
            self._handler.tick()


@dataclass(order=True)
class PrioritizedItem:
    output: TextDisplayableMessage = field(compare=False)
    priority: int
    msg_num: int


class TextHandler:
    """
    Generic event handler for printing the display output as text.
    """

    _msg_num = 0

    def __init__(self, display: Any):
        self._display = display
        self._queue = PriorityQueue()

    def handle(self, message: Dict[str, str]):
        def output_gen():
            return self._display.handle(message)

        self._enqueue(output_gen)

    def tick(self):
        def output_gen():
            return self._display.tick()

        self._enqueue(output_gen)
        while not self._queue.empty():
            item = self._queue.get(False)
            print(item.output, end="", flush=self._queue.empty())

    def _enqueue(self, output_gen: Callable[[], Generator]):
        for output in output_gen():
            if isinstance(output, tuple):
                output, priority = output
            else:
                priority = self._display.default_priority
            self._queue.put(PrioritizedItem(output, priority, self._msg_num), False)
            self._msg_num += 1
