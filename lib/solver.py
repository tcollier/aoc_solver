import json
import os
import traceback

from datetime import datetime

from lib.languages import language_config, all_languages
from lib.shell import ShellException, shell_out
from lib.solver_event import SolverEvent


class TerminationException(Exception):
    pass


class LanguageSolver(object):
    def __init__(self, conn, language, year, day, filename):
        self.conn = conn
        self.language = language
        self.year = year
        self.day = day
        self.filename = filename
        self.config = language_config(language)

    def __call__(self, expected, outfile):
        self._check_terminate()
        cmd = self._build()
        self._check_terminate()
        actual = self._solve(cmd)
        self._check_terminate()
        if not expected:
            self._handle_output(actual, outfile)
        elif actual == expected:
            self._handle_success(cmd)
        else:
            self._handle_invalid_output(expected, actual)

    def _check_terminate(self):
        if self.conn.poll():
            cmd = self.conn.recv()
            _args = self.conn.recv()
            if cmd == SolverEvent.TERMINATE:
                raise TerminationException()

    def _dispatch(self, event, args={}):
        args["language"] = self.language
        args["year"] = self.year
        args["day"] = self.day
        self.conn.send(event)
        self.conn.send(args)

    def _build(self):
        def curried_build():
            return self.config.cmd_fn(self.config.build_fn(self.filename))

        if not self.config.has_build_step():
            return curried_build()

        self._dispatch(SolverEvent.BUILD_START)
        try:
            cmd = curried_build()
            self._dispatch(SolverEvent.BUILD_END)
            return cmd
        except ShellException as e:
            self._dispatch(SolverEvent.BUILD_FAILED, {"stderr": e.stderr})
            raise e
        except Exception as e:
            self._dispatch(SolverEvent.BUILD_FAILED)
            traceback.print_exc()
            raise e

    def _solve(self, cmd):
        self._dispatch(SolverEvent.SOLVE_START)
        try:
            actual = shell_out(cmd)
            self._dispatch(SolverEvent.SOLVE_END)
            return actual
        except ShellException as e:
            self._dispatch(SolverEvent.SOLVE_ERRED, {"stderr": e.stderr})
            raise e
        except Exception as e:
            self._dispatch(SolverEvent.SOLVE_ERRED)
            traceback.print_exc()
            raise e

    def _handle_output(self, actual, outfile):
        self._dispatch(SolverEvent.SOLVE_ATTEMPTED, {"actual": actual})
        if outfile:
            open(outfile, "w").write(actual)
            self._dispatch(SolverEvent.OUTPUT_SAVED, {"file": outfile})

    def _handle_success(self, cmd):
        self._dispatch(SolverEvent.SOLVE_SUCCEEDED)
        if not self.config.timing:
            self._dispatch(SolverEvent.TIMING_SKIPPED)
            return
        self._dispatch(SolverEvent.TIMING_START)
        try:
            start_time = datetime.now()
            timing_info = json.loads(shell_out(f"{cmd} --time"))
            duration = datetime.now() - start_time
            self._dispatch(
                SolverEvent.TIMING_END, {"info": timing_info, "duration": duration}
            )
        except ShellException as e:
            self._dispatch(SolverEvent.TIMING_FAILED, {"stderr": e.stderr})
            raise e
        except Exception as e:
            self._dispatch(SolverEvent.TIMING_FAILED)
            traceback.print_exc()
            raise e

    def _handle_invalid_output(self, expected, actual):
        self._dispatch(
            SolverEvent.SOLVE_FAILED, {"expected": expected, "actual": actual}
        )


class Solver(object):
    def __init__(self, conn, year, day, save=False):
        if not os.path.isdir(year):
            raise ValueError(f"No source code exists for year {year}")
        padded_day = day.zfill(2)
        if not os.path.isdir(os.path.join(year, padded_day)):
            raise ValueError(f"No source code exists for day {day} in {year}")
        self.base_dir = os.path.join(year, padded_day)
        self.conn = conn
        self.year = year
        self.day = day
        self.save = save
        self.outfile = os.path.join(year, day.zfill(2), "output.txt")
        self.expected = None
        if os.path.isfile(self.outfile):
            self.expected = "".join(open(self.outfile, "r").readlines())

    @classmethod
    def has_solution(cls, year, day):
        return os.path.isfile(os.path.join(year, day.zfill(2), "output.txt"))

    def __call__(self, languages, save=False):
        found = False
        for language, filename in self._find_files(languages):
            found = True
            try:
                solver = LanguageSolver(
                    self.conn, language, self.year, self.day, filename
                )
                solver(self.expected, self.outfile if self.save else None)
            except KeyboardInterrupt as e:
                raise e
            except TerminationException:
                break
            except:
                continue
        if not found and languages:
            for language in languages:
                self._dispatch(SolverEvent.MISSING_SRC, {"language": language})

    def _dispatch(self, event, args={}):
        args["year"] = self.year
        args["day"] = self.day
        self.conn.send(event)
        self.conn.send(args)

    def _find_files(self, languages):
        if not languages:
            languages = all_languages()
        for language in languages:
            ext = language_config(language).extension
            filename = os.path.join(self.base_dir, f"main.{ext}")
            if os.path.isfile(filename):
                yield language, filename
