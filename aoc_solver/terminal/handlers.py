from dataclasses import dataclass
from typing import List

from aoc_solver.lang.registry import LanguageRegistry
from aoc_solver.solver_event import SolverEvent
from aoc_solver.terminal.elements import (
    CURSOR_RETURN,
    Box,
    BoxAlign,
    BoxDisplay,
    Element,
    ErrorText,
    Table,
    Text,
    TextColor,
)
from aoc_solver.terminal.registry import register_handler
from aoc_solver.types import PipeMessage, Stringable, StringableIterator

MAX_LANGUAGE_WIDTH = max([len(l) for l in LanguageRegistry.all()])


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
    details: Stringable = None

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
        for i in range(len(self.expected) - len(self.actual)):
            self.actual.append("")

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


def _handle_error(args):
    if "error" in args:
        yield Box(ErrorText(str(args["error"])), display=BoxDisplay.BLOCK)
    if "stdout" in args and args["stdout"]:
        # Node.js compilation errors are printed to STDOUT
        yield Box(ErrorText(args["stdout"]), display=BoxDisplay.BLOCK)
    if "stderr" in args and args["stderr"]:
        yield Box(ErrorText(args["stderr"]), display=BoxDisplay.BLOCK)


@register_handler(SolverEvent.MISSING_SRC)
def _missing_src(_display, args: PipeMessage) -> StringableIterator:
    yield StatusBox.build(
        StatusSettings.FAILED,
        args,
        details="(no source code found)",
        display=BoxDisplay.BLOCK,
    )


@register_handler(SolverEvent.BUILD_STARTED)
def _build_started(display, args: PipeMessage) -> StringableIterator:
    yield from display.set_busy(True)
    yield StatusBox.build(StatusSettings.COMPILING, args)


@register_handler(SolverEvent.BUILD_FINISHED)
def _build_finished(display, args: PipeMessage) -> StringableIterator:
    yield from display.set_busy(False)
    yield CURSOR_RETURN


@register_handler(SolverEvent.BUILD_FAILED)
def _build_failed(display, args: PipeMessage) -> StringableIterator:
    yield from display.set_busy(False)
    yield CURSOR_RETURN
    yield StatusBox.build(StatusSettings.FAILED, args, display=BoxDisplay.BLOCK)
    yield from _handle_error(args)


@register_handler(SolverEvent.SOLVE_STARTED)
def _solve_started(display, args: PipeMessage) -> StringableIterator:
    yield from display.set_busy(True)
    yield StatusBox.build(StatusSettings.SOLVING, args)


@register_handler(SolverEvent.SOLVE_FINISHED)
def _solve_finished(display, _args: PipeMessage) -> StringableIterator:
    yield from display.set_busy(False)
    yield CURSOR_RETURN


@register_handler(SolverEvent.SOLVE_FAILED)
def _solve_failed(display, args: PipeMessage) -> StringableIterator:
    yield from display.set_busy(False)
    yield CURSOR_RETURN
    yield StatusBox.build(StatusSettings.FAILED, args, display=BoxDisplay.BLOCK)
    yield from _handle_error(args)


@register_handler(SolverEvent.SOLVE_ATTEMPTED)
def _solve_attempted(_display, args: PipeMessage) -> StringableIterator:
    yield StatusBox.build(StatusSettings.ATTEMPTED, args, display=BoxDisplay.BLOCK)
    yield Table(
        [[Text("Output")], *[[Text(v)] for v in args["actual"].rstrip().split("\n")],]
    )


@register_handler(SolverEvent.SOLVE_SUCCEEDED)
def _solve_succeeded(_display, args: PipeMessage) -> StringableIterator:
    yield StatusBox.build(StatusSettings.SUCCEEDED, args)


@register_handler(SolverEvent.SOLVE_INCORRECT)
def _solve_incorrect(_display, args: PipeMessage) -> StringableIterator:
    yield StatusBox.build(StatusSettings.FAILED, args, display=BoxDisplay.BLOCK)
    yield DiffTable(
        args["expected"].rstrip().split("\n"), args["actual"].rstrip().split("\n")
    )


@register_handler(SolverEvent.OUTPUT_SAVED)
def _output_saved(_display, args: PipeMessage) -> StringableIterator:
    yield Box(Text(f"Saved result to {args['file']}"), display=BoxDisplay.BLOCK)


@register_handler(SolverEvent.TIMING_SKIPPED)
def _timing_skipped(_display, _args: PipeMessage):
    yield Box(Text(""), display=BoxDisplay.BLOCK)


@register_handler(SolverEvent.TIMING_STARTED)
def _timing_started(display, args: PipeMessage) -> StringableIterator:
    yield from display.set_busy(True)
    yield CURSOR_RETURN
    yield StatusBox.build(StatusSettings.TIMING, args)


@register_handler(SolverEvent.TIMING_FINISHED)
def _timing_finished(display, args: PipeMessage) -> StringableIterator:
    yield from display.set_busy(False)
    yield CURSOR_RETURN
    yield StatusBox.build(
        StatusSettings.SUCCEEDED,
        args,
        details=TimingDetails(args["info"], args["duration"]),
        display=BoxDisplay.BLOCK,
    )


@register_handler(SolverEvent.TIMING_FAILED)
def _timing_failed(display, args: PipeMessage) -> StringableIterator:
    yield from display.set_busy(False)
    yield CURSOR_RETURN
    yield StatusBox.build(StatusSettings.FAILED, args, display=BoxDisplay.BLOCK)
    yield from _handle_error(args)


@register_handler(SolverEvent.TERMINATE)
def _terminate(_display, args: PipeMessage) -> StringableIterator:
    if "error" in args:
        yield Box(Text(str(args["error"])), display=BoxDisplay.BLOCK)
