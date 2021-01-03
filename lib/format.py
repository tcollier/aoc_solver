from lib.languages import all_languages


class Color(object):
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    GREY = "\033[90m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def _decimal(number):
    parts = str(round(number, 2)).split(".")
    return ".".join([parts[0].rjust(3, " "), parts[1].rjust(2, "0")])


def _duration(duration):
    if duration < 1:
        return f"{Color.OKGREEN}{_decimal(duration * 1000)} ns{Color.ENDC}"
    elif duration < 1000:
        return f"{Color.OKCYAN}{_decimal(duration)} μs{Color.ENDC}"
    elif duration < 1000000:
        return f"{_decimal(duration / 1000)} ms"
    else:
        return f"{Color.WARNING}{_decimal(duration / 1000000)} s{Color.ENDC}"


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


def format_building(language, year, day):
    return _status(language, year, day, "COMP", Color.GREY)


def format_running(language, year, day):
    return _status(language, year, day, "EXEC", Color.OKCYAN)


def format_success(language, year, day):
    return _status(language, year, day, "PASS", Color.OKGREEN)


def format_failure(language, year, day):
    return _status(language, year, day, "FAIL", Color.FAIL)


def format_diff(expected, actual):
    exp_parts = expected.split("\n")
    act_parts = actual.split("\n")
    table = [[""], ["Expected"], ["Actual"]]
    if exp_parts[0] != act_parts[0]:
        table[0].append("Part 1")
        table[1].append(exp_parts[0])
        table[2].append(act_parts[0])
    if exp_parts[1] != act_parts[1]:
        table[0].append("Part 2")
        table[1].append(exp_parts[1])
        table[2].append(act_parts[1])
    return _table(table, {1: Color.OKCYAN, 2: Color.WARNING})


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
