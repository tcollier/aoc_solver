from lib.shell import is_process_running
from lib.solver_event import SolverEvent
from lib.typing import DisplayHandler, PipeConnection


class DisplayEventLoop(object):
    # The refresh rate (in frames per second) that the event loop will update
    # the display.
    REFRESH_RATE_FPS = 30

    def __init__(self, handler: DisplayHandler, conn: PipeConnection):
        self._handler = handler
        self._conn = conn

    def __call__(self, parent_pid: int):
        """
        :param parent_pid: Process ID of the parent that spawned the terminal
        display. Keep tabs on it so we can exit if it mysteriously vanishes,
        e.g. with a SIGKILL
        """
        running = True
        while running:
            if self._conn.poll(1 / self.REFRESH_RATE_FPS):
                message = self._conn.recv()
                event = message["event"]
                self._handler.handle(message)
                if event == SolverEvent.TERMINATE:
                    running = False
            if not is_process_running(parent_pid):
                self._handler.handle(
                    {
                        "event": SolverEvent.TERMINATE,
                        "error": "Main process has disappeared!",
                    }
                )
                running = False
            self._handler.tick()
