import os

from lib.lang.registry import LanguageSettings, register_language


@register_language(name="rust", extension="rs")
class RustSettings(LanguageSettings):
    LIB_DIR = os.path.join("lib", "rust")

    def compile(self):
        yield f"rustc -C opt-level=3 -o {self._bin_file} {self.file} -L {self.LIB_DIR}"

    def solve(self):
        return os.path.join(".", self._bin_file)
