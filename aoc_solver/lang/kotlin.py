import os

from aoc_solver.lang.registry import LanguageSettings, register_language


@register_language(name="kotlin", extension="kt")
class KotlinSettings(LanguageSettings):
    def __init__(self, file):
        self._jar_file = file.replace(".kt", ".jar")
        super(KotlinSettings, self).__init__(file)

    def compile(self):
        yield f"kotlinc {self.file} -include-runtime -d {self._jar_file}"

    def solve(self):
        return f"java -jar {self._jar_file}"
