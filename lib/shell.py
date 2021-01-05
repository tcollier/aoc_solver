import shlex
import subprocess
import time


class TerminationException(Exception):
    pass


class ShellException(Exception):
    def __init__(self, exitcode, stdout, stderr):
        self.exitcode = exitcode
        self.stdout = stdout
        self.stderr = stderr

    def __reduce__(self):
        return (ShellException, (self.exitcode, self.stdout, self.stderr))


def _read_output(stream):
    output = ""
    line = stream.readline()
    while line:
        output += line
        line = stream.readline()
    return output


def shell_out(cmd, should_terminate):
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
