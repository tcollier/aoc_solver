import os

from lib.lang.registry import LanguageSettings, register_language


@register_language(name="typescript", extension="ts")
class TypescriptSettings(LanguageSettings):
    ENTRY_FILE = os.path.join(".", "lib", "javascript", "index.js")

    def __init__(self, file):
        self._js_file = os.path.join(".", file.replace(".ts", ""))
        super(TypescriptSettings, self).__init__(file)

    def compile(self):
        yield f"yarn tsc {self.file}"

    def solve(self):
        return f"node {self.ENTRY_FILE} {self._js_file}"
