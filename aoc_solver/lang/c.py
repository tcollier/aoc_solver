import glob
import os

from aoc_solver import SOLUTIONS_ROOT
from aoc_solver.lang.registry import LanguageSettings, register_language


@register_language(name="c", extension="c")
class CSettings(LanguageSettings):
    LIB_FILES = glob.glob(
        os.path.join(SOLUTIONS_ROOT, "..", "aoc_executor.c", "src", "*.c")
    )

    def compile(self):
        yield f"gcc -O3 -o {self._bin_file} {self.file} {' '.join(self.LIB_FILES)}"

    def solve(self):
        return os.path.join(".", self._bin_file)
