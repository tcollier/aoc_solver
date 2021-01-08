from queue import SimpleQueue

from lib.languages import all_languages
from lib.shell import is_process_running
from lib.solver_event import SolverEvent
from lib.ui import Align, Box, Color, Decimal, Spinner, Table, TermText


def _duration(duration):
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
    return Box(TermText(f"{Decimal(value)} {unit}", color), 7 + len(unit), Align.RIGHT)


def _language(language):
    """
    Right pad the language name with spaces so that all languages will take up
    the same width.
    """
    max = 0
    for l in all_languages():
        if len(l) > max:
            max = len(l)
    return language.ljust(max, " ")


def _status(label, color, language, year, day):
    """
    Generic formatter for the solver's status of running the language/day
    """
    day_language = f"{year}/{day.rjust(2, '0')} {_language(language)}"
    return TermText(f"{label.ljust(4, ' ')} [{day_language}]", color)


def _attempt(language, year, day):
    return _status("TRY", Color.YELLOW, language, year, day)


def _building(language, year, day):
    return _status("COMP", Color.GREY, language, year, day)


def _solving(language, year, day):
    return _status("EXEC", Color.CYAN, language, year, day)


def _success(language, year, day):
    return _status("PASS", Color.GREEN, language, year, day)


def _failure(language, year, day):
    return _status("FAIL", Color.RED, language, year, day)


def _diff(expected, actual):
    exp_parts = expected.split("\n")
    act_parts = actual.split("\n")
    table = [[""], ["Expected"], ["Actual"]]
    if len(act_parts) < 1:
        table[0].append("Part 1")
        table[1].append(exp_parts[0])
        table[2].append("")
    elif exp_parts[0] != act_parts[0]:
        table[0].append("Part 1")
        table[1].append(exp_parts[0])
        table[2].append(act_parts[0])
    if len(act_parts) < 2:
        table[0].append("Part 2")
        table[1].append(exp_parts[1])
        table[2].append("")
    elif exp_parts[1] != act_parts[1]:
        table[0].append("Part 2")
        table[1].append(exp_parts[1])
        table[2].append(act_parts[1])
    return Table(table, {1: Color.CYAN, 2: Color.YELLOW})


def _timing(timing_info, duration):
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


def _split_args(args):
    return args["language"], args["year"], args["day"]


def _cursor_reset():
    return "\033[A\n"


class TerminalDisplay(object):
    def __init__(self):
        self.busy = False
        self._was_busy = False
        self._spinner = Spinner()
        self._queue = SimpleQueue()

    def handle(self, message):
        event = message["event"]
        handler = (
            self.HANDLERS[event] if event in self.HANDLERS else self._invalid_command
        )
        for output in handler(self, message):
            self._queue.put(output, False)

    def tick(self):
        if not self._was_busy and self.busy:
            self._queue.put(self._spinner.start())
            self._was_busy = True
        if self.busy:
            self._queue.put(self._spinner.tick())
        elif self._was_busy:
            print(self._spinner.stop(), end="", flush=True)
            self._was_busy = False
        while not self._queue.empty():
            text = self._queue.get(False)
            print(text, end="", flush=self._queue.empty())

    def _invalid_command(self, cmd, args):
        yield TermText(f"Invalid command {cmd} with arguments {args}", Color.RED)
        yield "\n"

    def _missing_src(self, args):
        language, year, day = _split_args(args)
        yield f"{_failure(language, year, day)} (no source code found)\n"
        yield "\n"

    def _build_started(self, args):
        self.busy = True
        language, year, day = _split_args(args)
        yield _building(language, year, day)

    def _build_finished(self, args):
        self.busy = False
        yield _cursor_reset()

    def _build_failed(self, args):
        self.busy = False
        language, year, day = _split_args(args)
        yield _cursor_reset()
        yield _failure(language, year, day)
        yield "\n"
        if "stdout" in args:
            yield args["stdout"]
        if "stderr" in args:
            yield args["stderr"]

    def _solve_started(self, args):
        language, year, day = _split_args(args)
        yield _solving(language, year, day)
        self.busy = True

    def _solve_finished(self, args):
        self.busy = False
        yield _cursor_reset()

    def _solve_failed(self, args):
        self.busy = False
        language, year, day = _split_args(args)
        yield _cursor_reset()
        yield _failure(language, year, day)
        yield "\n"
        if "stderr" in args:
            yield args["stderr"]

    def _solve_attempted(self, args):
        language, year, day = _split_args(args)
        yield _attempt(language, year, day)
        yield "\n"
        yield args["actual"].rstrip()
        yield "\n"

    def _solve_succeeded(self, args):
        language, year, day = _split_args(args)
        yield _success(language, year, day)

    def _solve_incorrect(self, args):
        language, year, day = _split_args(args)
        yield _failure(language, year, day)
        yield "\n"
        yield _diff(args["expected"], args["actual"])
        yield "\n"

    def _output_saved(self, args):
        yield f"Saved result to {args['file']}"
        yield "\n"

    def _timing_started(self, args):
        yield " "
        yield TermText(
            "timing", Color.GREY,
        )
        self.busy = True

    def _timing_skipped(self, args):
        yield "\n"

    def _timing_finished(self, args):
        self.busy = False
        language, year, day = _split_args(args)
        timing_info = _timing(args["info"], args["duration"])
        yield _cursor_reset()
        yield f"{_success(language, year, day)} {timing_info}"
        yield "\n"

    def _timing_failed(self, args):
        self.busy = False
        language, year, day = _split_args(args)
        yield _cursor_reset()
        yield _failure(language, year, day)
        yield "\n"
        if "stderr" in args:
            yield args["stderr"]

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
    }
