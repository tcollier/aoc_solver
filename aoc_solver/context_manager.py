from multiprocessing import Process

from aoc_solver.solver_event import SolverEvent
from aoc_solver.types import PipeConnection


class Context:
    """
    Container for all connections and processes managed in the file. Provides
    an easy way to clean up these resources when exiting the script.
    """

    conns = []
    procs = []

    def add_conn(self, conn: PipeConnection):
        self.conns.append(conn)

    def add_proc(self, proc: Process):
        proc.start()
        self.procs.append(proc)

    def shutdown(self, signal: int = None, error: str = None):
        """
        Send a TERMINATE event to all connections and join all processes
        to properly shutdown all resources.
        """
        while self.conns:
            conn = self.conns.pop()
            message = {"event": SolverEvent.TERMINATE}
            if signal:
                message["signal"] = signal
            if error:
                message["error"] = error
            conn.send(message)
            conn.close()
        while self.procs:
            proc = self.procs.pop()
            proc.join()


class ContextManager:
    """
    The class provides access to a global Context so we can shutdown from
    anywhere in this script.
    """

    _context = Context()

    @classmethod
    def add_conn(cls, conn: PipeConnection):
        cls._context.add_conn(conn)

    @classmethod
    def add_proc(cls, proc: Process):
        cls._context.add_proc(proc)

    @classmethod
    def shutdown(cls, signal: int = None, error: str = None):
        cls._context.shutdown(signal, error)
