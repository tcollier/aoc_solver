from queue import PriorityQueue


class PrioritizedItem(object):
    def __init__(self, output, msg_num, priority):
        self.output = output
        self.msg_num = msg_num
        self.priority = priority

    def __lt__(self, other):
        if self.priority == other.priority:
            return self.msg_num < other.msg_num
        else:
            return self.priority < other.priority


class TextHandler(object):
    def __init__(self, display):
        self._display = display
        self._queue = PriorityQueue()
        self._msg_num = 0

    def handle(self, message):
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

    def _enqueue(self, output_gen):
        for output in output_gen():
            if isinstance(output, tuple):
                output, priority = output
            else:
                priority = self._display.default_priority
            self._queue.put(PrioritizedItem(output, self._msg_num, priority), False)
            self._msg_num += 1
