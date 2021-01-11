import glob
import os

from lib.lang.registry import LanguageSettings, register_language

AOC_ROOT = os.path.abspath(
    os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    )
)


@register_language(name="scala", extension="scala")
class ScalaSettings(LanguageSettings):
    LIB_DIR = os.path.join(AOC_ROOT, "lib", "scala")
    LIB_SRC = glob.glob(os.path.join(LIB_DIR, "**", "*.java"))

    def compile(self):
        yield f"scalac -optimize -d {self.LIB_DIR} {' '.join(self.LIB_SRC)}"
        yield f"scalac  -d {self._base_dir} -classpath {self.LIB_DIR} {self.file}"

    def solve(self):
        return f"scala -classpath {self._base_dir}:{self.LIB_DIR} Main"
