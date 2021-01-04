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


def _time_with_spinner(cmd, pipe):
    def fn():
        start_time = datetime.now()
        timing_info = json.loads(shell_out(f"{cmd} --time"))
        duration = datetime.now() - start_time
        return format_timing(timing_info, duration)

    print(f"{Color.GREY}timing{Color.ENDC} ", end="", flush=True)
    fn_with_spinner(fn, pipe)


def _solve_with_spinner(cmd, pipe):
    def fn():
        return shell_out(cmd)

    fn_with_spinner(fn, pipe)


def _build_with_spinner(config, filename, pipe):
    def fn():
        return config.cmd_fn(config.build_fn(filename))

    fn_with_spinner(fn, pipe)


def _build(config, filename, language, year, day):
    if not config.has_build_step():
        return config.cmd_fn(config.build_fn(filename))

    print(format_building(language, year, day), end=" ", flush=True)
    try:
        cmd = concurrent_with_spinner(_build_with_spinner, config, filename)
        print("\033[A")
        return cmd
    except ShellException as e:
        print("\033[A")
        print(format_failure(language, year, day), end="  \n")
        print(e.stderr, end="")
        raise e
    except Exception as e:
        print("\033[A")
        print(format_failure(language, year, day), end="  \n")
        traceback.print_exc()
        raise e


def _run(cmd, language, year, day):
    print(format_running(language, year, day), end=" ", flush=True)
    try:
        actual = concurrent_with_spinner(_solve_with_spinner, cmd)
        print("\033[A")  # Move cursor back to start of line
        return actual
    except ShellException as e:
        print("\033[A")
        print(format_failure(language, year, day), end="  \n")
        print(e.stderr)
        raise e
    except Exception as e:
        print("\033[A")
        print(format_failure(language, year, day), end="  \n")
        traceback.print_exc()
        raise e


def _handle_attempt(language, year, day, actual, save):
    print("\033[A")
    print(format_attempt(language, year, day), end="  \n")
    print(actual.rstrip())
    if save:
        outfile = _output_file(year, day)
        open(outfile, "w").write(actual)
        print(f"Saved result to {outfile}")


def _handle_success(config, cmd, language, year, day):
    print(
        format_success(language, year, day),
        end=" " if config.timing else "",
        flush=True,
    )
    if not config.timing:
        print("  ")  # Overwrite the spinner and add new line
        return
    try:
        timing_info = concurrent_with_spinner(_time_with_spinner, cmd)
        print("\033[A")
        print(f"{format_success(language, year, day)} {timing_info}")
    except ShellException as e:
        print("\033[A")
        print(format_failure(language, year, day), end="  \n")
        print(e.stderr)
        raise e
    except Exception as e:
        print("\033[A")
        print(format_failure(language, year, day), end="  \n")
        traceback.print_exc()
        raise e


def _handle_bad_output(language, year, day, expected, actual):
    print(format_failure(language, year, day), end="  \n")
    print(format_diff(expected, actual))


def solve(languages, year, day, save=False):
    outfile = _output_file(year, day)
    expected = _find_solution(outfile)
    if expected and save:
        raise Exception(
            f"Cannot save results when {outfile} alread exists, please delete it"
        )
    found = False
    for l, filename in _find_files(languages, year, day):
        found = True
        config = language_config(l)
        try:
            cmd = _build(config, filename, l, year, day)
            actual = _run(cmd, l, year, day)
            if not expected:
                _handle_attempt(l, year, day, actual, save)
            elif actual == expected:
                _handle_success(config, cmd, l, year, day)
            else:
                _handle_bad_output(l, year, day, expected, actual)
        except KeyboardInterrupt as e:
            raise e
        except:
            continue
    if not found and languages:
        for l in languages:
            print(f"{format_failure(l, year, day)} (no {l} source code found)")
