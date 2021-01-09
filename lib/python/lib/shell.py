import os
import shlex
import subprocess
import time

from typing import IO


class TerminationException(Exception):
    pass


class ShellException(Exception):
    def __init__(self, exitcode: int, stdout: str, stderr: str):
        self.exitcode = exitcode
        self.stdout = stdout
        self.stderr = stderr

    def __reduce__(self):
        return (ShellException, (self.exitcode, self.stdout, self.stderr))


def _read_output(stream: IO[str]) -> str:
    output = ""
    line = stream.readline()
    while line:
        output += line
        line = stream.readline()
    return output


def shell_out(cmd: str, should_terminate: bool):
    process = subprocess.Popen(
        shlex.split(cmd),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )
    while True:
        exitcode = process.poll()
        if exitcode is None:
            if should_terminate():
                raise TerminationException()
            time.sleep(0.01)
        elif exitcode > 0:
            stdout = _read_output(process.stdout)
            stderr = _read_output(process.stderr)
            raise ShellException(exitcode, stdout, stderr)
        else:
            break
    return _read_output(process.stdout)


def is_process_running(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False
