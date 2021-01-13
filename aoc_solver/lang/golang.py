import os

from aoc_solver import SOLUTIONS_ROOT
from aoc_solver.lang.registry import LanguageSettings, register_language


@register_language(name="golang", extension="go")
class GolangSettings(LanguageSettings):
    LIB_PATH = os.path.abspath(os.path.join(SOLUTIONS_ROOT, "..", "aoc_executor.go"))

    def compile(self):
        actual_path = os.environ.get("GOPATH") and os.path.abspath(
            os.environ.get("GOPATH")
        )
        if not actual_path or actual_path != self.LIB_PATH:
            message = (
                f"Please set the following environment variable\nGOPATH={self.LIB_PATH}"
            )
            raise Exception(message)
        yield f"go build -pkgdir {self.LIB_PATH} -o {self._bin_file} {self.file}"

    def solve(self):
        return os.path.join(".", self._bin_file)
