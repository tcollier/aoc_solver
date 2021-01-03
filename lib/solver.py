import json
import multiprocessing
import os
import time
import traceback

from datetime import datetime

from lib.format import (
    Color,
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


# The spinner expects the following pipe messages to be recv'd/sent
#
#   1. Send `True` message to tell spinner to start
#   2. Send `True` message to tell spinner to stop
#   3. Recv `True` message to indicate spinner is finished
#
def _concurrent_spinner(pipe):
    spinners = ["⣷", "⣯", "⣟", "⡿", "⢿", "⣻", "⣽", "⣾"]
    index = 0
    pipe.recv()
    waiting = True
    print(" ", end="")
    while waiting:
        print(f"\b{spinners[index]}", end="", flush=True)
        index = (index + 1) % len(spinners)
        if pipe.poll(0.08):
            pipe.recv()
            waiting = False
    print("\b", end="")
    pipe.send(True)


def _time_cmd(cmd, pipe):
    timing_str = "timing"
    print(f"{Color.GREY}{timing_str}{Color.ENDC} ", end="", flush=True)
    pipe.send(True)  # Tell spinner to start
    start_time = datetime.now()
    timing_info = json.loads(shell_out(f"{cmd} --time"))
    duration = datetime.now() - start_time
    pipe.send(True)  # Tell spinner to stop
    pipe.recv()  # Wait for spinner to finish
    print("\b" * (len(timing_str) + 1), end="")
    print(format_timing(timing_info, duration))


def _concurrent_time_cmd(cmd):
    pipe1, pipe2 = multiprocessing.Pipe(True)
    tproc = multiprocessing.Process(target=_time_cmd, args=(cmd, pipe1))
    tproc.start()
    wproc = multiprocessing.Process(target=_concurrent_spinner, args=(pipe2,))
    wproc.start()
    wproc.join()
    tproc.join()
    pipe1.close()
    pipe2.close()


def _solve(cmd, pipe):
    pipe.send(True)  # Tell spinner to start
    try:
        actual = shell_out(cmd)
    except ShellException as e:
        actual = e
    pipe.send(True)  # Tell spinner to stop
    pipe.recv()  # Wait for spinner to finish
    pipe.send(actual)


def _concurrent_solve(cmd):
    pipe1, pipe2 = multiprocessing.Pipe(True)
    tproc = multiprocessing.Process(target=_solve, args=(cmd, pipe1))
    tproc.start()
    wproc = multiprocessing.Process(target=_concurrent_spinner, args=(pipe2,))
    wproc.start()
    wproc.join()
    tproc.join()
    actual = pipe2.recv()
    pipe1.close()
    pipe2.close()
    if isinstance(actual, Exception):
        raise actual
    else:
        return actual


def _build(config, filename, pipe):
    pipe.send(True)
    try:
        cmd = config.cmd_fn(config.build_fn(filename))
    except ShellException as e:
        cmd = e
    pipe.send(True)
    pipe.recv()
    pipe.send(cmd)


def _concurrent_build(config, filename):
    pipe1, pipe2 = multiprocessing.Pipe(True)
    tproc = multiprocessing.Process(target=_build, args=(config, filename, pipe1))
    tproc.start()
    wproc = multiprocessing.Process(target=_concurrent_spinner, args=(pipe2,))
    wproc.start()
    wproc.join()
    tproc.join()
    cmd = pipe2.recv()
    pipe1.close()
    pipe2.close()
    if isinstance(cmd, Exception):
        raise cmd
    else:
        return cmd


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
                cmd = _concurrent_build(config, filename)
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
            actual = _concurrent_solve(cmd)
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
                    _concurrent_time_cmd(cmd)
                else:
                    print("  ")  # Overwrite the spinner and add new line
            else:
                print(format_failure(l, year, day))
                print(format_diff(expected, actual))
        else:
            print(actual.rstrip())
            if save:
                open(outfile, "w").write(actual)
                print(f"Saved reault to {outfile}")
    if not found and language:
        for l in language:
            print(f"{format_failure(l, year, day)} (no {l} source code found)")
