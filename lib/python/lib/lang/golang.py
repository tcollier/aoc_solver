import glob
import os

from lib.lang.registry import LanguageSettings, register_language


@register_language(name="golang", extension="go", timing=False)
class GolangSettings(LanguageSettings):
    def compile(self):
        yield f"go build -o {self._bin_file} {self.file}"

    def solve(self):
        return os.path.join(".", self._bin_file)
