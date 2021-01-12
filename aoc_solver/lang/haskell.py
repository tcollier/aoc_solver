import os

from aoc_solver.lang.registry import LanguageSettings, register_language


@register_language(name="haskell", extension="hs", timing=False)
class HaskellSettings(LanguageSettings):
    def compile(self):
        yield f"ghc -o {self._bin_file} {self.file}"

    def solve(self):
        return os.path.join(".", self._bin_file)
