import json

from datetime import datetime
from typing import Callable, Dict, List, Union

Input = Union[List[str], List[int]]
SolverCallable = Callable[[Input], str]


class Executor:
    def __init__(self, data: Input, part1_fn: SolverCallable, part2_fn: SolverCallable):
        self.data = data
        self.part1_fn = part1_fn
        self.part2_fn = part2_fn

    def __call__(self, argv: List[str]):
        if argv[-1] == "--time":
            self._time()
        else:
            self._solve()

    def _solve(self):
        print(self.part1_fn([v for v in self.data]))
        print(self.part2_fn([v for v in self.data]))

    def _time(self):
        print(
            json.dumps(
                {
                    "part1": self._time_fn(self.part1_fn),
                    "part2": self._time_fn(self.part2_fn),
                }
            )
        )

    def _time_fn(self, fn: SolverCallable) -> Dict:
        def duration_us(duration):
            return duration.seconds * 1000 * 1000 + duration.microseconds

        def continue_timing(iterations, duration):
            if iterations < 100:
                return duration < 30000000
            else:
                return duration < 100000

        i = 0
        running_time = 0
        while continue_timing(i, running_time):
            data = [v for v in self.data]
            start_time = datetime.now()
            fn(data)
            running_time += duration_us(datetime.now() - start_time)
            i += 1
        return {"duration": running_time, "iterations": i}
