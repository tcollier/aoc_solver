import shlex
import subprocess


class ShellException(Exception):
    def __init__(self, message, stderr):
        self.message = message
        self.stderr = stderr
        super(ShellException, self).__init__(message)

    def __reduce__(self):
        return (ShellException, (self.message, self.stderr))


def shell_out(cmd):
    process = subprocess.Popen(
        shlex.split(cmd),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )
    stdout = ""
    stderr = ""
    while True:
        stdout += process.stdout.readline()
        stderr += process.stderr.readline()
        return_code = process.poll()
        if return_code is None:
            continue
        elif return_code > 0:
            line = process.stderr.readline()
            while line:
                stderr += line
                line = process.stderr.readline()
            raise ShellException(
                f"Command '{cmd}' exited with status code {return_code}", stderr
            )
        else:
            stdout += process.stdout.readline()
        break
    return stdout
