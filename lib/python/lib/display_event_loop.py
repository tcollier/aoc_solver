from __future__ import annotations
from queue import PriorityQueue
from typing import Callable, Dict, Generator

from lib.shell import is_process_running
from lib.solver_event import SolverEvent
from lib.typing import TextDisplay, PipeConnection


class DisplayEventLoop(object):
    def __init__(
        self, display: TextDisplay, conn: PipeConnection, refresh_rate: int = 30
    ):
        """
        :param refresh_rate: rate (in frames per second) at which events are process
        and thus the maximum rate the display will be updated.
        """
        self._handler = TextHandler(display)
        self._conn = conn
        self._refresh_rate = refresh_rate

    def __call__(self, parent_pid: int):
        """
        :param parent_pid: Process ID of the parent that spawned the terminal
        display. Keep tabs on it so we can exit if it mysteriously vanishes,
        e.g. with a SIGKILL
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


class PrioritizedItem(object):
    def __init__(self, output, msg_num: int, priority: int):
        self.output = output
        self.msg_num = msg_num
        self.priority = priority

    def __lt__(self, other: PrioritizedItem):
        if self.priority == other.priority:
            return self.msg_num < other.msg_num
        else:
            return self.priority < other.priority


class TextHandler(object):
    """
    Generic event handler for printing the display output as text.
    """

    def __init__(self, display: Display):
        self._display = display
        self._queue = PriorityQueue()
        self._msg_num = 0

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
            self._queue.put(PrioritizedItem(output, self._msg_num, priority), False)
            self._msg_num += 1
