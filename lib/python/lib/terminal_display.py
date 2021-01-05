from multiprocessing import Pipe, Process

from lib.languages import all_languages
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
    FPS = 12

    def __init__(self, conn):
        self.conn = conn
        self.index = 0

    def start(self):
        self.index = 0
        print(" ", end="")
        while True:
            print(f"\b{self.CHARS[self.index]}", end="", flush=True)
            self.index = (self.index + 1) % len(self.CHARS)
            if self.conn.poll(1 / self.FPS):
                self.conn.recv()
                break
        print("\b", end="", flush=True)
        self.conn.send(True)
        self.conn.close()


def _decimal(number):
    parts = str(round(number, 2)).split(".")
    return ".".join([parts[0].rjust(3, " "), parts[1].rjust(2, "0")])


def _duration(duration):
    if duration < 1:
        return f"{Color.GREEN}{_decimal(duration * 1000)} ns{Color.ENDC}"
    elif duration < 1000:
        return f"{_decimal(duration)} μs"
    elif duration < 1000000:
        return f"{Color.YELLOW}{_decimal(duration / 1000)} ms{Color.ENDC}"
    else:
        return f"{Color.RED}{_decimal(duration / 1000000)} s{Color.ENDC}"


def _language(language):
    max = 0
    for l in all_languages():
        if len(l) > max:
            max = len(l)
    return language.ljust(max, " ")


def _header(value, width):
    if not value:
        return " " * (width)
    underlined = f"{Color.UNDERLINE}{value}{Color.ENDC}"
    width += len(Color.UNDERLINE) + len(Color.ENDC)
    lpad = " " * ((width - len(underlined)) // 2)
    rpad = " " * (width - len(underlined) - len(lpad))
    return f"{lpad}{underlined}{rpad}"


def _cell(value, width, color):
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
                string += _header(table[row][col], col_width[col])
            else:
                string += _cell(table[row][col], col_width[col], row_colors[row])
            string += "  " if col < len(table[row]) - 1 else ""
        string += "\n"
    return string


def _status(language, year, day, label, color):
    day_language = f"{year}/{day.rjust(2, '0')} {_language(language)}"
    return f"{color}{label} [{day_language}]{Color.ENDC}"


def format_attempt(language, year, day):
    return _status(language, year, day, "TRY ", Color.YELLOW)


def format_building(language, year, day):
    return _status(language, year, day, "COMP", Color.GREY)


def format_solving(language, year, day):
    return _status(language, year, day, "EXEC", Color.CYAN)


def format_success(language, year, day):
    return _status(language, year, day, "PASS", Color.GREEN)


def format_failure(language, year, day):
    return _status(language, year, day, "FAIL", Color.RED)


def format_diff(expected, actual):
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


def format_timing(timing_info, duration):
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


def _handle_invalid_command(cmd, args):
    print(_colorize(Color.RED, f"Invalid command {cmd} with arguments {args}"))


def _handle_missing_src(_, args):
    language, year, day = _split_args(args)
    print(f"{format_failure(language, year, day)} (no source code found)")


def _handle_build_start(display, args):
    language, year, day = _split_args(args)
    print(format_building(language, year, day), end=" ", flush=True)
    display.start_spinner()


def _handle_build_end(display, args):
    display.stop_spinner()
    print("\033[A")


def _handle_build_failed(display, args):
    display.stop_spinner()
    language, year, day = _split_args(args)
    print("\033[A")
    print(format_failure(language, year, day), end="  \n")
    if "stdout" in args:
        print(args["stdout"], end="")
    if "stderr" in args:
        print(args["stderr"], end="")


def _handle_solve_start(display, args):
    language, year, day = _split_args(args)
    print(format_solving(language, year, day), end=" ", flush=True)
    display.start_spinner()


def _handle_solve_end(display, args):
    display.stop_spinner()
    print("\033[A")


def _handle_solve_erred(display, args):
    display.stop_spinner()
    language, year, day = _split_args(args)
    print("\033[A")
    print(format_failure(language, year, day), end="  \n")
    if "stderr" in args:
        print(args["stderr"], end="")


def _handle_solve_attempted(_, args):
    language, year, day = _split_args(args)
    print(format_attempt(language, year, day), end="  \n")
    print(args["actual"].rstrip())


def _handle_solve_succeeded(_, args):
    language, year, day = _split_args(args)
    print(
        format_success(language, year, day), end=" ", flush=True,
    )


def _handle_solved_failed(_, args):
    language, year, day = _split_args(args)
    print(format_failure(language, year, day), end="  \n")
    print(format_diff(args["expected"], args["actual"]))


def _handle_output_saved(_, args):
    print(f"Saved result to {args['file']}")


def _handle_timing_start(display, args):
    print(_colorize(Color.GREY, "timing"), end=" ")
    display.start_spinner()


def _handle_timing_skipped(_, args):
    print("  ")  # Overwrite the spinner and add new line


def _handle_timing_end(display, args):
    display.stop_spinner()
    language, year, day = _split_args(args)
    timing_info = format_timing(args["info"], args["duration"])
    print("\033[A")
    print(f"{format_success(language, year, day)} {timing_info}")


def _handle_timing_failed(display, args):
    display.stop_spinner()
    language, year, day = _split_args(args)
    print("\033[A")
    print(format_failure(language, year, day), end="  \n")
    if "stderr" in args:
        print(args["stderr"], end="")


HANDLERS = {
    SolverEvent.MISSING_SRC: _handle_missing_src,
    SolverEvent.BUILD_START: _handle_build_start,
    SolverEvent.BUILD_END: _handle_build_end,
    SolverEvent.BUILD_FAILED: _handle_build_failed,
    SolverEvent.SOLVE_START: _handle_solve_start,
    SolverEvent.SOLVE_END: _handle_solve_end,
    SolverEvent.SOLVE_SUCCEEDED: _handle_solve_succeeded,
    SolverEvent.SOLVE_ERRED: _handle_solve_erred,
    SolverEvent.SOLVE_ATTEMPTED: _handle_solve_attempted,
    SolverEvent.SOLVE_FAILED: _handle_solved_failed,
    SolverEvent.OUTPUT_SAVED: _handle_output_saved,
    SolverEvent.TIMING_START: _handle_timing_start,
    SolverEvent.TIMING_SKIPPED: _handle_timing_skipped,
    SolverEvent.TIMING_END: _handle_timing_end,
    SolverEvent.TIMING_FAILED: _handle_timing_failed,
}


class TerminalDisplay(object):
    def __init__(self, conn):
        self.conn = conn
        self.spinner_conn = None
        self.spinner_proc = None

    def start_spinner(self):
        if self.spinner_conn:
            return
        self.spinner_conn, conn = Pipe()
        spinner = Spinner(conn)
        self.spinner_proc = Process(target=spinner.start, name="Spinner", daemon=True)
        self.spinner_proc.start()

    def stop_spinner(self):
        if not self.spinner_conn:
            return
        self.spinner_conn.send(True)
        self.spinner_conn.recv()
        self.spinner_proc.join()
        self.spinner_conn.close()
        self.spinner_conn = None

    def __call__(self):
        running = True
        while running:
            if self.conn.poll(0.01):
                cmd = self.conn.recv()
                args = self.conn.recv()
                if cmd in HANDLERS:
                    HANDLERS[cmd](self, args)
                elif cmd == SolverEvent.TERMINATE:
                    running = False
                    self.stop_spinner()
                    if "error" in args:
                        print(args["error"])
                else:
                    _handle_invalid_command(cmd, args)
