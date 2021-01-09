from typing import Generator, Tuple, Union

from lib.languages import all_languages
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
from lib.typing import PipeMessage, TextDisplayableHandler

SPINNER_CHARS = ["⣷", "⣯", "⣟", "⡿", "⢿", "⣻", "⣽", "⣾"]


class MessagePriority:
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
        color = TextColor.GREEN
    elif duration < 1000:
        value = duration
        unit = "μs"
        color = None
    elif duration < 1000000:
        value = duration / 1000
        unit = "ms"
        color = TextColor.YELLOW
    else:
        value = duration / 1000000
        unit = "s"
        color = TextColor.RED
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


def _status_box(
    label: str,
    color: TextColor,
    args: PipeMessage,
    details: str = None,
    display: BoxDisplay = BoxDisplay.INLINE,
) -> Element:
    """
    Generic formatter for the solver's status of running the language/day
    """
    language = args["language"]
    year = args["year"]
    day = args["day"]
    day_language = f"{year}/{str(day).rjust(2, '0')} {_language(language)}"
    status = Text(f"{label.ljust(4, ' ')} [{day_language}]", color)
    if details:
        status = Text(" ".join([str(status), details]))
    return Box(status, display=display)


def _success_box(
    args: PipeMessage, details: str = None, display: BoxDisplay = BoxDisplay.INLINE,
) -> Element:
    return _status_box("PASS", TextColor.GREEN, args, details=details, display=display)


def _failure_box(args: PipeMessage, details: str = None) -> Element:
    return _status_box(
        "FAIL", TextColor.RED, args, details=details, display=BoxDisplay.BLOCK
    )


def _diff_table(expected: str, actual: str) -> Element:
    exp_parts = expected.split("\n")
    act_parts = actual.split("\n")
    if act_parts[0] is None:
        act_parts[0] = ""
    if act_parts[1] is None:
        act_parts[1] = ""
    exp_color = TextColor.CYAN
    act_color = TextColor.YELLOW
    table = [[Text("")], [Text("Expected", exp_color)], [Text("Actual", act_color)]]
    if exp_parts[0] != act_parts[0]:
        table[0].append(Text("Part 1"))
        table[1].append(Text(exp_parts[0], exp_color))
        table[2].append(Text(act_parts[0], act_color))
    if exp_parts[1] != act_parts[1]:
        table[0].append(Text("Part 2"))
        table[1].append(Text(exp_parts[1], exp_color))
        table[2].append(Text(act_parts[1], act_color))
    return Table(table, display=BoxDisplay.BLOCK)


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
        yield _failure_box(args, details="(no source code found)")

    def _build_started(self, args: PipeMessage) -> TextDisplayableHandler:
        yield from self._start_spinner()
        yield _status_box("COMP", TextColor.GREY, args)

    def _build_finished(self, args: PipeMessage) -> TextDisplayableHandler:
        yield from self._clear_spinner()
        yield CURSOR_RETURN

    def _build_failed(self, args: PipeMessage) -> TextDisplayableHandler:
        yield from self._clear_spinner()
        yield CURSOR_RETURN
        yield _failure_box(args)
        if "stdout" in args:
            yield Box(Text(args["stdout"]), display=BoxDisplay.BLOCK)
        if "stderr" in args:
            yield Box(Text(args["stderr"]), display=BoxDisplay.BLOCK)

    def _solve_started(self, args: PipeMessage) -> TextDisplayableHandler:
        yield from self._start_spinner()
        yield _status_box("EXEC", TextColor.CYAN, args)

    def _solve_finished(self, args: PipeMessage) -> TextDisplayableHandler:
        yield from self._clear_spinner()
        yield CURSOR_RETURN

    def _solve_failed(self, args: PipeMessage) -> TextDisplayableHandler:
        yield from self._clear_spinner()
        yield CURSOR_RETURN
        yield _failure_box(args)
        if "stderr" in args:
            yield Box(Text(args["stderr"]), display=BoxDisplay.BLOCK)

    def _solve_attempted(self, args: PipeMessage) -> TextDisplayableHandler:
        yield _status_box("TRY", TextColor.YELLOW, args, display=BoxDisplay.BLOCK)
        yield Table(
            [
                [Text("Output")],
                *[[Text(v)] for v in args["actual"].rstrip().split("\n")],
            ]
        )

    def _solve_succeeded(self, args: PipeMessage) -> TextDisplayableHandler:
        yield _success_box(args)

    def _solve_incorrect(self, args: PipeMessage) -> TextDisplayableHandler:
        yield _failure_box(args)
        yield _diff_table(args["expected"], args["actual"])

    def _output_saved(self, args: PipeMessage) -> TextDisplayableHandler:
        yield Box(Text(f"Saved result to {args['file']}"), display=BoxDisplay.BLOCK)

    def _timing_skipped(self, *_):
        yield Box(Text(""), display=BoxDisplay.BLOCK)

    def _timing_started(self, args: PipeMessage) -> TextDisplayableHandler:
        yield from self._start_spinner()
        yield Text(" ")
        yield Text("timing", TextColor.GREY)

    def _timing_finished(self, args: PipeMessage) -> TextDisplayableHandler:
        yield from self._clear_spinner()
        yield CURSOR_RETURN
        yield _success_box(
            args,
            details=_timing(args["info"], args["duration"]),
            display=BoxDisplay.BLOCK,
        )

    def _timing_failed(self, args: PipeMessage) -> TextDisplayableHandler:
        yield from self._clear_spinner()
        yield CURSOR_RETURN
        yield _failure_box(args)
        if "stderr" in args:
            yield Box(Text(args["stderr"]), display=BoxDisplay.BLOCK)

    def _terminate(self, args: PipeMessage) -> TextDisplayableHandler:
        if "error" in args:
            yield Box(Text(args["error"]), display=BoxDisplay.BLOCK)

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
