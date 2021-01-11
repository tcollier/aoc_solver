import os

from lib.lang.registry import LanguageSettings, register_language

AOC_ROOT = os.path.abspath(
    os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    )
)


@register_language(name="typescript", extension="ts")
class TypescriptSettings(LanguageSettings):
    ENTRY_FILE = os.path.join(AOC_ROOT, "lib", "javascript", "index.js")

    def __init__(self, file):
        self._js_file = file.replace(".ts", "")
        super(TypescriptSettings, self).__init__(file)

    def compile(self):
        yield f"yarn tsc {self.file}"

    def solve(self):
        return f"node {self.ENTRY_FILE} {self._js_file}"
