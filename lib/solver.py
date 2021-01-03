import json
import multiprocessing
import os
import time

from datetime import datetime

from lib.format import format_diff, format_failure, format_success, format_timing
from lib.languages import language_config, all_languages
from lib.shell import shell_out


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
    start_time = datetime.now()
    timing_info = json.loads(shell_out(f"{cmd} --time"))
    duration = datetime.now() - start_time
    pipe.send(True)
    pipe.recv()
    print(format_timing(timing_info, duration))
    pipe.close()


def _concurrent_spinner(pipe):
    spinners = ["/", "-", "\\", "|"]
    index = 0
    waiting = True
    print(" ", end="")
    while waiting:
        print(f"\b{spinners[index]}", end="", flush=True)
        index = (index + 1) % len(spinners)
        if pipe.poll(0.1):
            pipe.recv()
            waiting = False
    print("\b", end="")
    pipe.send(True)


def _concurrent_time_cmd(cmd):
    pipe1, pipe2 = multiprocessing.Pipe(True)
    tproc = multiprocessing.Process(target=_time_cmd, args=(cmd, pipe1))
    tproc.start()
    wproc = multiprocessing.Process(target=_concurrent_spinner, args=(pipe2,))
    wproc.start()
    wproc.join()
    tproc.join()


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
        cmd = config.cmd_fn(config.build_fn(filename))
        actual = shell_out(cmd)
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
                print(format_failure(l, year, day))
                print(format_diff(expected, actual))
        else:
            print(actual.rstrip())
            if save:
                open(outfile, "w").write(actual)
                print(f"Saved reault to {outfile}")
    if not found and language:
        for l in language:
            print(f"{format_failure(l, year, day)} (no source code found {l})")
