from typing import Generator, Tuple, Union

from lib.languages import all_languages
from lib.solver_event import SolverEvent
from lib.terminal.ui import (
    CURSOR_RETURN,
    Animation,
    Box,
    BoxAlign,
    Color,
    Element,
    Table,
    Text,
)
from lib.typing import PipeMessage

TextDisplayable = Union[str, Element]
TextDisplayableMessage = Union[TextDisplayable, Tuple[TextDisplayable, int]]
TextDisplayableHandler = Generator[TextDisplayableMessage, None, None]

SPINNER_CHARS = ["⣷", "⣯", "⣟", "⡿", "⢿", "⣻", "⣽", "⣾"]


class Priority:
    LOW = 2
    MEDIUM = 1
    HIGH = 0


def _duration(duration: float) -> Element:
    """
    Convert the duration from microseconds to the unit that will allow the
    number to be between 1 <= n < 1,000 and apply the unit (e.g. "ms") and
    any colorization.

    :param duration: time in microseconds
    """
    if duration < 1:
        value = duration * 1000
        unit = "ns"
        color = Color.GREEN
    elif duration < 1000:
        value = duration
        unit = "μs"
        color = None
    elif duration < 1000000:
        value = duration / 1000
        unit = "ms"
        color = Color.YELLOW
    else:
        value = duration / 1000000
        unit = "s"
        color = Color.RED
    formatted_value = "{:.2f}".format(value)
    box_width = len(f"NNN.NN {unit}")
    return Box(Text(f"{formatted_value} {unit}", color), box_width, BoxAlign.RIGHT)


def _language(language: str) -> Element:
    """
    Right pad the language name with spaces so that all languages will take up
    the same width.
    """
    max = 0
    for l in all_languages():
        if len(l) > max:
            max = len(l)
    return Box(Text(language), max)


def _status(label: str, color: Color, args: PipeMessage) -> Element:
    """
    Generic formatter for the solver's status of running the language/day
    """
    language = args["language"]
    year = args["year"]
    day = args["day"]
    day_language = f"{year}/{str(day).rjust(2, '0')} {_language(language)}"
    return Text(f"{label.ljust(4, ' ')} [{day_language}]", color)


def _success(args: PipeMessage) -> Element:
    return _status("PASS", Color.GREEN, args)


def _failure(args: PipeMessage) -> Element:
    return _status("FAIL", Color.RED, args)


def _diff(expected: str, actual: str) -> Element:
    exp_parts = expected.split("\n")
    act_parts = actual.split("\n")
    if act_parts[0] is None:
        act_parts[0] = ""
    if act_parts[1] is None:
        act_parts[1] = ""
    exp_color = Color.CYAN
    act_color = Color.YELLOW
    table = [[Text("")], [Text("Expected", exp_color)], [Text("Actual", act_color)]]
    if exp_parts[0] != act_parts[0]:
        table[0].append(Text("Part 1"))
        table[1].append(Text(exp_parts[0], exp_color))
        table[2].append(Text(act_parts[0], act_color))
    if exp_parts[1] != act_parts[1]:
        table[0].append(Text("Part 2"))
        table[1].append(Text(exp_parts[1], exp_color))
        table[2].append(Text(act_parts[1], act_color))
    return Table(table)


def _timing(timing_info: dict, duration: float) -> str:
    duration_us = duration.seconds * 1000000 + duration.microseconds
    overhead = (
        duration_us
        - timing_info["part1"]["duration"]
        - timing_info["part2"]["duration"]
    )
    part1_avg_time = (
        timing_info["part1"]["duration"] / timing_info["part1"]["iterations"]
    )
    part2_avg_time = (
        timing_info["part2"]["duration"] / timing_info["part2"]["iterations"]
    )
    part2_spacer = " " if part1_avg_time >= 1000000 else ""
    overhead_spacer = " " if part2_avg_time >= 1000000 else ""
    end_spacer = " " if overhead >= 1000000 else ""
    contents = ", ".join(
        [
            f"part1: {_duration(part1_avg_time)}",
            f"{part2_spacer}part2: {_duration(part2_avg_time)}",
            f"{overhead_spacer}overhead: {_duration(overhead)}{end_spacer}",
        ]
    )
    return f"({contents})"


class Display:
    def __init__(self):
        self._spinner = Animation(SPINNER_CHARS)

    def handle(self, message: PipeMessage) -> TextDisplayableHandler:
        event = message["event"]
        handler = (
            self.HANDLERS[event] if event in self.HANDLERS else self._invalid_command
        )
        yield from handler(self, message)

    def tick(self) -> TextDisplayableHandler:
        if self._spinner.active:
            yield (self._spinner.tick(), Priority.LOW)

    @property
    def default_priority(self) -> int:
        return Priority.MEDIUM

    def _start_spinner(self) -> TextDisplayableHandler:
        if not self._spinner.active:
            yield (" ", Priority.LOW)
            yield (self._spinner.start(), Priority.LOW)

    def _clear_spinner(self) -> TextDisplayableHandler:
        if self._spinner.active:
            yield (self._spinner.clear(), Priority.HIGH)

    def _invalid_command(_self, cmd: str, args: PipeMessage) -> TextDisplayableHandler:
        yield Text(f"Invalid command {cmd} with arguments {args}", Color.RED)
        yield "\n"

    def _missing_src(_self, args: PipeMessage) -> TextDisplayableHandler:
        yield f"{_failure(args)} (no source code found)"
        yield "\n"

    def _build_started(self, args: PipeMessage) -> TextDisplayableHandler:
        yield from self._start_spinner()
        yield _status("COMP", Color.GREY, args)

    def _build_finished(self, args: PipeMessage) -> TextDisplayableHandler:
        yield from self._clear_spinner()
        yield CURSOR_RETURN

    def _build_failed(self, args: PipeMessage) -> TextDisplayableHandler:
        yield from self._clear_spinner()
        yield CURSOR_RETURN
        yield _failure(args)
        yield "\n"
        if "stdout" in args:
            yield args["stdout"]
        if "stderr" in args:
            yield args["stderr"]

    def _solve_started(self, args: PipeMessage) -> TextDisplayableHandler:
        yield from self._start_spinner()
        yield _status("EXEC", Color.CYAN, args)

    def _solve_finished(self, args: PipeMessage) -> TextDisplayableHandler:
        yield from self._clear_spinner()
        yield CURSOR_RETURN

    def _solve_failed(self, args: PipeMessage) -> TextDisplayableHandler:
        yield from self._clear_spinner()
        yield CURSOR_RETURN
        yield _failure(args)
        yield "\n"
        if "stderr" in args:
            yield args["stderr"]

    def _solve_attempted(self, args: PipeMessage) -> TextDisplayableHandler:
        yield _status("TRY", Color.YELLOW, args)
        yield "\n"
        yield args["actual"].rstrip()
        yield "\n"

    def _solve_succeeded(self, args: PipeMessage) -> TextDisplayableHandler:
        yield _success(args)

    def _solve_incorrect(self, args: PipeMessage) -> TextDisplayableHandler:
        yield _failure(args)
        yield "\n"
        yield _diff(args["expected"], args["actual"])
        yield "\n"

    def _output_saved(self, args: PipeMessage) -> TextDisplayableHandler:
        yield f"Saved result to {args['file']}"
        yield "\n"

    def _timing_started(self, args: PipeMessage) -> TextDisplayableHandler:
        yield from self._start_spinner()
        yield " "
        yield Text("timing", Color.GREY)

    def _timing_skipped(self, args: PipeMessage) -> TextDisplayableHandler:
        yield "\n"

    def _timing_finished(self, args: PipeMessage) -> TextDisplayableHandler:
        yield from self._clear_spinner()
        yield CURSOR_RETURN
        yield f"{_success(args)} {_timing(args['info'], args['duration'])}"
        yield "\n"

    def _timing_failed(self, args: PipeMessage) -> TextDisplayableHandler:
        yield from self._clear_spinner()
        yield CURSOR_RETURN
        yield _failure(args)
        yield "\n"
        if "stderr" in args:
            yield args["stderr"]

    def _terminate(self, args: PipeMessage) -> TextDisplayableHandler:
        if "error" in args:
            yield args["error"]
        else:
            yield "Unknown error occurred. Terminating..."
        yield "\n"

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
