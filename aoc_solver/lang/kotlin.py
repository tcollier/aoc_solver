import glob
import os

from aoc_solver import AOC_ROOT
from aoc_solver.lang.registry import LanguageSettings, register_language


@register_language(name="kotlin", extension="kt")
class KotlinSettings(LanguageSettings):
    SRC_DIR = os.path.join(os.path.dirname(AOC_ROOT), "aoc_executor.kt", "src")
    SRC_FILES = glob.glob(os.path.join(SRC_DIR, "**", "*.kt"))

    def __init__(self, file):
        self._jar_file = file.replace(".kt", ".jar")
        super(KotlinSettings, self).__init__(file)

    def compile(self):
        yield f"kotlinc {self.file} {' '.join(self.SRC_FILES)} -include-runtime -d {self._jar_file}"

    def solve(self):
        return f"java -jar {self._jar_file}"
