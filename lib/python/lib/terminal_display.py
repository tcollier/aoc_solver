from multiprocessing import Pipe, Process

from lib.languages import all_languages
from lib.shell import is_process_running
from lib.solver_event import SolverEvent


class Color(object):
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    GREY = "\033[90m"
    ENDC = "\033[0m"
    UNDERLINE = "\033[4m"


class Spinner(object):
    CHARS = ["⣷", "⣯", "⣟", "⡿", "⢿", "⣻", "⣽", "⣾"]

    def __init__(self):
        self.index = 0
        print(" ", end="")

    def tick(self):
        print(f"\b{self.CHARS[self.index]}", end="", flush=True)
        self.index = (self.index + 1) % len(self.CHARS)

    def stop(self):
        print("\b", end="", flush=True)


def _table_header(value, width):
    if not value:
        return " " * (width)
    underlined = f"{Color.UNDERLINE}{value}{Color.ENDC}"
    width += len(Color.UNDERLINE) + len(Color.ENDC)
    lpad = " " * ((width - len(underlined)) // 2)
    rpad = " " * (width - len(underlined) - len(lpad))
    return f"{lpad}{underlined}{rpad}"


def _table_cell(value, width, color):
    if color:
        colored = f"{color}{value}{Color.ENDC}"
        width += len(color) + len(Color.ENDC)
    else:
        colored = value

    try:
        int(value)
        justified = colored.rjust(width, " ")
    except:
        justified = colored.ljust(width, " ")
    return f"{justified}"


def _table(table, row_colors):
    col_width = [0 for _ in table[0]]
    for row in range(len(table)):
        for col in range(len(table[row])):
            if len(table[row][col]) > col_width[col]:
                col_width[col] = len(table[row][col])
    string = ""
    for row in range(len(table)):
        for col in range(len(table[row])):
            if row == 0:
                string += _table_header(table[row][col], col_width[col])
            else:
                string += _table_cell(table[row][col], col_width[col], row_colors[row])
            string += "  " if col < len(table[row]) - 1 else ""
        string += "\n"
    return string


def _decimal(number):
    """
    Format a decimal to be right justified with 2 digits to the right of
    the decimal place and left padded with spaces to take up 3 characters
    to the left.
    """
    parts = str(round(number, 2)).split(".")
    return ".".join([parts[0].rjust(3, " "), parts[1].ljust(2, "0")])


def _duration(duration):
    """
    Convert the duratino from microseconds to the unit that will allow the
    number to be between 1 <= n < 1,000 and apply the unit (e.g. "ms") and
    any colorization.

    :param duration: time in microseconds
    """
    if duration < 1:
        return f"{Color.GREEN}{_decimal(duration * 1000)} ns{Color.ENDC}"
    elif duration < 1000:
        return f"{_decimal(duration)} μs"
    elif duration < 1000000:
        return f"{Color.YELLOW}{_decimal(duration / 1000)} ms{Color.ENDC}"
    else:
        return f"{Color.RED}{_decimal(duration / 1000000)} s{Color.ENDC}"


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
    return f"{color}{label} [{day_language}]{Color.ENDC}"


def _attempt(language, year, day):
    return _status("TRY ", Color.YELLOW, language, year, day)


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
    return _table(table, {1: Color.CYAN, 2: Color.YELLOW})


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


def _colorize(color, string):
    return f"{color}{string}{Color.ENDC}"


def _split_args(args):
    return args["language"], args["year"], args["day"]


def _cursor_reset():
    print("\033[A")


class TerminalDisplay(object):
    # The refresh rate (in frames per second) that the event loop will update
    # the display. The only animation to speak of is the spinner, so the
    # primary effect of changing this value will be changing the speed that
    # the spinner spins.
    REFRESH_RATE_FPS = 15

    def __init__(self, conn):
        self.conn = conn
        self.spinner = None

    def start_spinner(self):
        if self.spinner:
            return
        self.spinner = Spinner()

    def stop_spinner(self):
        if not self.spinner:
            return
        self.spinner.stop()
        self.spinner = None

    def __call__(self, parent_pid):
        """
        :param parent_pid: Process ID of the parent that spawned the terminal
        self. Keep tabs on it so we can exit if it mysteriously vanishes,
        e.g. with a SIGKILL
        """
        running = True
        while running:
            if self.conn.poll(1 / self.REFRESH_RATE_FPS):
                cmd = self.conn.recv()
                args = self.conn.recv()
                if cmd in self.HANDLERS:
                    self.HANDLERS[cmd](self, args)
                elif cmd == SolverEvent.TERMINATE:
                    running = False
                    self.stop_spinner()
                    if "error" in args:
                        print(args["error"])
                else:
                    self._invalid_command(cmd, args)
            if not is_process_running(parent_pid):
                running = False
                self.stop_spinner()
            if self.spinner:
                self.spinner.tick()

    def _invalid_command(self, cmd, args):
        print(_colorize(Color.RED, f"Invalid command {cmd} with arguments {args}"))

    def _missing_src(self, args):
        language, year, day = _split_args(args)
        print(f"{_failure(language, year, day)} (no source code found)")

    def _build_started(self, args):
        language, year, day = _split_args(args)
        print(_building(language, year, day), end=" ", flush=True)
        self.start_spinner()

    def _build_finished(self, args):
        self.stop_spinner()
        _cursor_reset()

    def _build_failed(self, args):
        self.stop_spinner()
        language, year, day = _split_args(args)
        _cursor_reset()
        print(_failure(language, year, day), end="  \n")
        if "stdout" in args:
            print(args["stdout"], end="")
        if "stderr" in args:
            print(args["stderr"], end="")

    def _solve_started(self, args):
        language, year, day = _split_args(args)
        print(_solving(language, year, day), end=" ", flush=True)
        self.start_spinner()

    def _solve_finished(self, args):
        self.stop_spinner()
        _cursor_reset()

    def _solve_failed(self, args):
        self.stop_spinner()
        language, year, day = _split_args(args)
        _cursor_reset()
        print(_failure(language, year, day), end="  \n")
        if "stderr" in args:
            print(args["stderr"], end="")

    def _solve_attempted(self, args):
        language, year, day = _split_args(args)
        print(_attempt(language, year, day), end="  \n")
        print(args["actual"].rstrip())

    def _solve_succeeded(self, args):
        language, year, day = _split_args(args)
        print(
            _success(language, year, day), end=" ", flush=True,
        )

    def _solve_incorrect(self, args):
        language, year, day = _split_args(args)
        print(_failure(language, year, day), end="  \n")
        print(_diff(args["expected"], args["actual"]))

    def _output_saved(self, args):
        print(f"Saved result to {args['file']}")

    def _timing_started(self, args):
        print(_colorize(Color.GREY, "timing"), end=" ")
        self.start_spinner()

    def _timing_skipped(self, args):
        print("  ")  # Overwrite the spinner and add new line

    def _timing_finished(self, args):
        self.stop_spinner()
        language, year, day = _split_args(args)
        timing_info = _timing(args["info"], args["duration"])
        _cursor_reset()
        print(f"{_success(language, year, day)} {timing_info}")

    def _timing_failed(self, args):
        self.stop_spinner()
        language, year, day = _split_args(args)
        _cursor_reset()
        print(_failure(language, year, day), end="  \n")
        if "stderr" in args:
            print(args["stderr"], end="")

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
