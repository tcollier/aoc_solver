import glob
import os

from aoc_solver import SOLUTIONS_ROOT
from aoc_solver.lang.registry import LanguageSettings, register_language


@register_language(name="scala", extension="scala")
class ScalaSettings(LanguageSettings):
    LIB_DIR = os.path.join(SOLUTIONS_ROOT, "..", "aoc_executor.scala", "src")
    LIB_SRC = glob.glob(os.path.join(LIB_DIR, "**", "*.scala"))

    def compile(self):
        yield f"scalac -optimize -d {self.LIB_DIR} {' '.join(self.LIB_SRC)}"
        yield f"scalac -d {self._base_dir} -classpath {self.LIB_DIR} {self.file}"

    def solve(self):
        return f"scala -classpath {self._base_dir}:{self.LIB_DIR} Main"
