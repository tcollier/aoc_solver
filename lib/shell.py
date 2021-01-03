import shlex
import subprocess


def shell_out(cmd):
    process = subprocess.Popen(
        shlex.split(cmd), stdout=subprocess.PIPE, universal_newlines=True
    )
    stdout = ""
    while True:
        stdout += process.stdout.readline()
        return_code = process.poll()
        if return_code is None:
            continue
        elif return_code > 0:
            print(stdout)
            raise Exception(f"Command '{cmd}' exited with status code {return_code}")
        else:
            stdout += process.stdout.readline()
        break
    return stdout
