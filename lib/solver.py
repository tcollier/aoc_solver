import json
import os

from datetime import datetime

from lib.format import format_diff, format_failure, format_success, format_timing
from lib.languages import LANGUAGES, language_list
from lib.shell import shell_out


def find_files(language, year, day):
    languages = language if language else LANGUAGES.keys()
    for l in languages:
        if l not in LANGUAGES.keys():
            raise Exception(f"Unrecognized language: {l} (available: {language_list})")
    if not os.path.isdir(year):
        raise Exception(f"Invalid year {year}")
    padded_day = day.zfill(2)
    if not os.path.isdir(os.path.join(year, padded_day)):
        raise Exception(f"Invalid day {day} for {year}")
    found = False
    for l in languages:
        filename = os.path.join(year, padded_day, f"main.{LANGUAGES[l].extension}")
        if os.path.isfile(filename):
            found = True
            yield l, filename
        elif language:
            raise Exception(f"File for langage {l} does not exist: {filename}")
    if not found:
        raise Exception(f"No source files found in {os.path.join(year, padded_day)}")


def output_file(year, day):
    return os.path.join(year, day.zfill(2), "output.txt")


def find_solution(filename):
    if os.path.isfile(filename):
        return "".join(open(filename, "r").readlines())
    else:
        return None


def solve(language, year, day, save):
    outfile = output_file(year, day)
    expected = find_solution(outfile)
    if expected and save:
        raise Exception(
            f"Cannot save results when {outfile} alread exists, please delete it"
        )
    for language, filename in find_files(language, year, day):
        config = LANGUAGES[language]
        cmd = config.cmd_fn(config.build_fn(filename))
        actual = shell_out(cmd)
        if expected:
            if actual == expected:
                if config.timing:
                    start_time = datetime.now()
                    timing_info = json.loads(shell_out(f"{cmd} --time"))
                    duration = datetime.now() - start_time
                    print(
                        f"{format_success(language, year, day)} ({format_timing(timing_info, duration)})"
                    )
                else:
                    print(format_success(language, year, day))
            else:
                print(format_failure(language, year, day))
                print(format_diff(expected, actual))
        else:
            print(actual.rstrip())
            if save:
                open(outfile, "w").write(actual)
                print(f"Saved reault to {outfile}")
