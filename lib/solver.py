import json
import os
import time
import traceback

from datetime import datetime

from lib.concurrency import concurrent_with_spinner, fn_with_spinner
from lib.format import (
    Color,
    format_attempt,
    format_building,
    format_diff,
    format_failure,
    format_running,
    format_success,
    format_timing,
)
from lib.languages import language_config, all_languages
from lib.shell import ShellException, shell_out


def _find_files(language, year, day):
    languages = language if language else all_languages()
    for l in languages:
        if l not in all_languages():
            raise Exception(
                f"Unrecognized language: {l} (available: {', '.join(all_languages())})"
            )
    if not os.path.isdir(year):
        raise Exception(f"Invalid year {year}")
    padded_day = day.zfill(2)
    if not os.path.isdir(os.path.join(year, padded_day)):
        raise Exception(f"Invalid day {day} for {year}")
    found = False
    for l in languages:
        filename = os.path.join(
            year, padded_day, f"main.{language_config(l).extension}"
        )
        if os.path.isfile(filename):
            found = True
            yield l, filename


def _output_file(year, day):
    return os.path.join(year, day.zfill(2), "output.txt")


def _find_solution(filename):
    if os.path.isfile(filename):
        return "".join(open(filename, "r").readlines())
    else:
        return None


def _time_cmd(cmd, pipe):
    def fn():
        start_time = datetime.now()
        timing_info = json.loads(shell_out(f"{cmd} --time"))
        duration = datetime.now() - start_time
        return format_timing(timing_info, duration)

    print(f"{Color.GREY}timing{Color.ENDC} ", end="", flush=True)
    fn_with_spinner(fn, pipe)


def _solve(cmd, pipe):
    def fn():
        return shell_out(cmd)

    fn_with_spinner(fn, pipe)


def _build(config, filename, pipe):
    def fn():
        return config.cmd_fn(config.build_fn(filename))

    fn_with_spinner(fn, pipe)


def solve(language, year, day, save=False):
    outfile = _output_file(year, day)
    expected = _find_solution(outfile)
    if expected and save:
        raise Exception(
            f"Cannot save results when {outfile} alread exists, please delete it"
        )
    found = False
    for l, filename in _find_files(language, year, day):
        found = True
        config = language_config(l)
        if config.has_build_step():
            print(format_building(l, year, day), end=" ", flush=True)
            try:
                cmd = concurrent_with_spinner(_build, config, filename)
                print("\033[A")
            except ShellException as e:
                print("\033[A")
                print(format_failure(l, year, day), end="  \n")
                print(e.stderr, end="")
                continue
        else:
            cmd = config.cmd_fn(config.build_fn(filename))
        print(format_running(l, year, day), end=" ", flush=True)
        try:
            actual = concurrent_with_spinner(_solve, cmd)
            print("\033[A")  # Move cursor back to start of line
        except ShellException as e:
            print("\033[A")
            print(format_failure(l, year, day), end="  \n")
            print(e.stderr)
            continue
        if expected:
            if actual == expected:
                print(
                    format_success(l, year, day),
                    end=" " if config.timing else "",
                    flush=True,
                )
                if config.timing:
                    try:
                        timing_info = concurrent_with_spinner(_time_cmd, cmd)
                        print("\033[A")
                        print(f"{format_success(l, year, day)} {timing_info}")
                    except ShellException as e:
                        print("\033[A")
                        print(format_failure(l, year, day), end="  \n")
                        print(e.stderr)
                        continue
                else:
                    print("  ")  # Overwrite the spinner and add new line
            else:
                print(format_failure(l, year, day), end="  \n")
                print(format_diff(expected, actual))
        else:
            print("\033[A")
            print(format_attempt(l, year, day), end="  \n")
            print(actual.rstrip())
            if save:
                open(outfile, "w").write(actual)
                print(f"Saved reault to {outfile}")
    if not found and language:
        for l in language:
            print(f"{format_failure(l, year, day)} (no {l} source code found)")
