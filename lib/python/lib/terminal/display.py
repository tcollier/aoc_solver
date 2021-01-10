from dataclasses import dataclass
from typing import Generator, List, Tuple, Union

from lib.lang.registry import LanguageRegistry
from lib.solver_event import SolverEvent
from lib.terminal.ui import (
    CURSOR_RETURN,
    Animation,
    Box,
    BoxAlign,
    BoxDisplay,
    TextColor,
    Element,
    Table,
    Text,
)
from lib.typing import PipeMessage, TextDisplayable, TextDisplayableHandler

SPINNER_CHARS = ["⣷", "⣯", "⣟", "⡿", "⢿", "⣻", "⣽", "⣾"]

MAX_LANGUAGE_WIDTH = max([len(l) for l in LanguageRegistry.all()])


class MessagePriority:
    LOW = 2
    MEDIUM = 1
    HIGH = 0


@dataclass
class Solution:
    year: int
    day: int
    language: str

    @classmethod
    def from_args(_cls, args):
        return Solution(args["year"], args["day"], args["language"])


@dataclass
class StatusBox(Element):
    status: str
    color: str
    solution: Solution
    display: BoxDisplay
    details: TextDisplayable = None

    @classmethod
    def build(_cls, settings, args, display=BoxDisplay.INLINE, details=None):
        status, color = settings
        return StatusBox(status, color, Solution.from_args(args), display, details)

    def __repr__(self):
        formatted_day = f"{self.solution.year}/{str(self.solution.day).rjust(2, '0')}"
        formatted_language = Box(Text(self.solution.language), width=MAX_LANGUAGE_WIDTH)
        day_language = f"{formatted_day} {formatted_language}"
        status = Text(f"{self.status.ljust(4, ' ')} [{day_language}]", self.color)
        if self.details:
            status = Text(" ".join([str(status), str(self.details)]))
        return str(Box(status, display=self.display))


class StatusSettings:
    COMPILING = ("COMP", TextColor.GREY)
    SOLVING = ("EXEC", TextColor.CYAN)
    TIMING = ("TIME", TextColor.MAGENTA)
    ATTEMPTED = ("TRY", TextColor.YELLOW)
    SUCCEEDED = ("PASS", TextColor.GREEN)
    FAILED = ("FAIL", TextColor.RED)


@dataclass
class TimingDuration(Element):
    """
    Convert the duration from microseconds to the unit that will allow the
    number to be between 1 <= n < 1,000 and apply the unit (e.g. "ms") and
    any colorization.

    :param duration: time in microseconds
    """

    duration: float

    def __repr__(self):
        if self.duration < 1:
            value = self.duration * 1000
            unit = "ns"
            color = TextColor.GREEN
        elif self.duration < 1000:
            value = self.duration
            unit = "μs"
            color = None
        elif self.duration < 1000000:
            value = self.duration / 1000
            unit = "ms"
            color = TextColor.YELLOW
        else:
            value = self.duration / 1000000
            unit = "s"
            color = TextColor.RED
        formatted_value = "{:.2f}".format(value)
        box_width = len(f"NNN.NN {unit}")
        return str(
            Box(Text(f"{formatted_value} {unit}", color), box_width, BoxAlign.RIGHT)
        )


@dataclass
class TimingDetails(Element):
    # Dictionary that contains "part1" and "part2" keys, both of which point to objects
    # that have "iterations" (number of times the solver function was inovked) and
    # "duration" (total time in microseconds all iterations took)
    timing_info: dict
    duration: float

    def _avg_time(self, part: str) -> float:
        return self.timing_info[part]["duration"] / self.timing_info[part]["iterations"]

    @property
    def _timing_duration(self):
        return (
            self.timing_info["part1"]["duration"]
            + self.timing_info["part2"]["duration"]
        )

    def __repr__(self):
        duration_us = self.duration.seconds * 1000000 + self.duration.microseconds
        overhead = duration_us - self._timing_duration
        part1_avg_time = self._avg_time("part1")
        part2_avg_time = self._avg_time("part2")
        part2_spacer = " " if part1_avg_time >= 1000000 else ""
        overhead_spacer = " " if part2_avg_time >= 1000000 else ""
        end_spacer = " " if overhead >= 1000000 else ""
        contents = ", ".join(
            [
                f"part1: {TimingDuration(part1_avg_time)}",
                f"{part2_spacer}part2: {TimingDuration(part2_avg_time)}",
                f"{overhead_spacer}overhead: {TimingDuration(overhead)}{end_spacer}",
            ]
        )
        return f"({contents})"


class DiffTable(Element):
    EXPECTED_COLOR = TextColor.CYAN
    ACTUAL_COLOR = TextColor.YELLOW

    def __init__(self, expected: List[str], actual: List[str]):
        self.expected = expected
        self.actual = actual
        for i in range(len(self.expected)):
            if self.actual[i] is None:
                self.actual[i] = ""

    def __repr__(self):
        table = [
            [Text("")],
            [Text("Expected", self.EXPECTED_COLOR)],
            [Text("Actual", self.ACTUAL_COLOR)],
        ]
        for i in range(len(self.expected)):
            if self.expected[i] != self.actual[i]:
                table[0].append(Text(f"Part {i + 1}"))
                table[1].append(Text(self.expected[i], self.EXPECTED_COLOR))
                table[2].append(Text(self.actual[i], self.ACTUAL_COLOR))
        return str(Table(table, display=BoxDisplay.BLOCK))


class Display:
    _spinner = Animation(SPINNER_CHARS)

    def handle(self, message: PipeMessage) -> TextDisplayableHandler:
        event = message["event"]
        handler = (
            self.HANDLERS[event] if event in self.HANDLERS else self._invalid_command
        )
        yield from handler(self, message)

    def tick(self) -> TextDisplayableHandler:
        if self._spinner.active:
            yield (self._spinner.tick(), MessagePriority.LOW)

    @property
    def default_priority(self) -> int:
        return MessagePriority.MEDIUM

    def _start_spinner(self) -> TextDisplayableHandler:
        if not self._spinner.active:
            yield (" ", MessagePriority.LOW)
            yield (self._spinner.start(), MessagePriority.LOW)

    def _clear_spinner(self) -> TextDisplayableHandler:
        if self._spinner.active:
            yield (self._spinner.clear(), MessagePriority.HIGH)

    def _invalid_command(_self, cmd: str, args: PipeMessage) -> TextDisplayableHandler:
        yield Box(
            Text(f"Invalid command {cmd} with arguments {args}", TextColor.RED),
            display=BoxDisplay.BLOCK,
        )

    def _missing_src(_self, args: PipeMessage) -> TextDisplayableHandler:
        yield StatusBox.build(
            StatusSettings.FAILED,
            args,
            details="(no source code found)",
            display=BoxDisplay.BLOCK,
        )

    def _build_started(self, args: PipeMessage) -> TextDisplayableHandler:
        yield from self._start_spinner()
        yield StatusBox.build(StatusSettings.COMPILING, args)

    def _build_finished(self, args: PipeMessage) -> TextDisplayableHandler:
        yield from self._clear_spinner()
        yield CURSOR_RETURN

    def _build_failed(self, args: PipeMessage) -> TextDisplayableHandler:
        yield from self._clear_spinner()
        yield CURSOR_RETURN
        yield StatusBox.build(StatusSettings.FAILED, args, display=BoxDisplay.INLINE)
        if "stdout" in args:
            yield Box(Text(args["stdout"]), display=BoxDisplay.BLOCK)
        if "stderr" in args:
            yield Box(Text(args["stderr"]), display=BoxDisplay.BLOCK)

    def _solve_started(self, args: PipeMessage) -> TextDisplayableHandler:
        yield from self._start_spinner()
        yield StatusBox.build(StatusSettings.SOLVING, args)

    def _solve_finished(self, args: PipeMessage) -> TextDisplayableHandler:
        yield from self._clear_spinner()
        yield CURSOR_RETURN

    def _solve_failed(self, args: PipeMessage) -> TextDisplayableHandler:
        yield from self._clear_spinner()
        yield CURSOR_RETURN
        yield StatusBox.build(StatusSettings.FAILED, args, display=BoxDisplay.BLOCK)
        if "stderr" in args:
            yield Box(Text(args["stderr"]), display=BoxDisplay.BLOCK)

    def _solve_attempted(self, args: PipeMessage) -> TextDisplayableHandler:
        yield StatusBox.build(StatusSettings.ATTEMPTED, args, display=BoxDisplay.BLOCK)
        yield Table(
            [
                [Text("Output")],
                *[[Text(v)] for v in args["actual"].rstrip().split("\n")],
            ]
        )

    def _solve_succeeded(self, args: PipeMessage) -> TextDisplayableHandler:
        yield StatusBox.build(StatusSettings.SUCCEEDED, args)

    def _solve_incorrect(self, args: PipeMessage) -> TextDisplayableHandler:
        yield StatusBox.build(StatusSettings.FAILED, args, display=BoxDisplay.BLOCK)
        yield DiffTable(
            args["expected"].rstrip().split("\n"), args["actual"].rstrip().split("\n")
        )

    def _output_saved(self, args: PipeMessage) -> TextDisplayableHandler:
        yield Box(Text(f"Saved result to {args['file']}"), display=BoxDisplay.BLOCK)

    def _timing_skipped(self, *_):
        yield Box(Text(""), display=BoxDisplay.BLOCK)

    def _timing_started(self, args: PipeMessage) -> TextDisplayableHandler:
        yield from self._start_spinner()
        yield CURSOR_RETURN
        yield StatusBox.build(StatusSettings.TIMING, args)

    def _timing_finished(self, args: PipeMessage) -> TextDisplayableHandler:
        yield from self._clear_spinner()
        yield CURSOR_RETURN
        yield StatusBox.build(
            StatusSettings.SUCCEEDED,
            args,
            details=TimingDetails(args["info"], args["duration"]),
            display=BoxDisplay.BLOCK,
        )

    def _timing_failed(self, args: PipeMessage) -> TextDisplayableHandler:
        yield from self._clear_spinner()
        yield CURSOR_RETURN
        yield StatusBox.build(StatusSettings.FAILED, args, display=BoxDisplay.BLOCK)
        if "stderr" in args:
            yield Box(Text(args["stderr"]), display=BoxDisplay.BLOCK)

    def _terminate(self, args: PipeMessage) -> TextDisplayableHandler:
        if "error" in args:
            yield Box(Text(str(args["error"])), display=BoxDisplay.BLOCK)

    HANDLERS = {
        SolverEvent.MISSING_SRC: _missing_src,
        SolverEvent.BUILD_STARTED: _build_started,
        SolverEvent.BUILD_FINISHED: _build_finished,
        SolverEvent.BUILD_FAILED: _build_failed,
        SolverEvent.SOLVE_STARTED: _solve_started,
        SolverEvent.SOLVE_FINISHED: _solve_finished,
        SolverEvent.SOLVE_SUCCEEDED: _solve_succeeded,
        SolverEvent.SOLVE_FAILED: _solve_failed,
        SolverEvent.SOLVE_ATTEMPTED: _solve_attempted,
        SolverEvent.SOLVE_INCORRECT: _solve_incorrect,
        SolverEvent.OUTPUT_SAVED: _output_saved,
        SolverEvent.TIMING_STARTED: _timing_started,
        SolverEvent.TIMING_SKIPPED: _timing_skipped,
        SolverEvent.TIMING_FINISHED: _timing_finished,
        SolverEvent.TIMING_FAILED: _timing_failed,
        SolverEvent.TERMINATE: _terminate,
    }
