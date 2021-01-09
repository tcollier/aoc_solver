from __future__ import annotations
from queue import PriorityQueue
from typing import Callable, Dict, Generator

from lib.typing import Display


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
