import glob
import os

from lib.lang.registry import LanguageSettings, register_language

AOC_ROOT = os.path.abspath(
    os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    )
)


@register_language(name="c", extension="c")
class CSettings(LanguageSettings):
    LIB_FILES = glob.glob(os.path.join(AOC_ROOT, "lib", "c", "*.c"))

    def compile(self):
        yield f"gcc -O3 -o {self._bin_file} {self.file} {' '.join(self.LIB_FILES)}"

    def solve(self):
        return os.path.join(".", self._bin_file)
