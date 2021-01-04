import multiprocessing

from lib.shell import ShellException, shell_out

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


def fn_with_spinner(fn, pipe):
    pipe.send(True)  # Tell spinner to start
    try:
        result = fn()
    except Exception as e:
        result = e
    pipe.send(True)  # Tell spinner to stop
    pipe.recv()  # Wait for spinner to finish
    pipe.send(result)


def concurrent_with_spinner(fn, *args):
    pipe1, pipe2 = multiprocessing.Pipe(True)
    fn_proc = multiprocessing.Process(target=fn, args=(*args, pipe1))
    fn_proc.start()
    spinner_proc = multiprocessing.Process(target=_concurrent_spinner, args=(pipe2,))
    spinner_proc.start()
    spinner_proc.join()
    fn_proc.join()
    result = pipe2.recv()
    pipe1.close()
    pipe2.close()
    if isinstance(result, Exception):
        raise result
    else:
        return result
