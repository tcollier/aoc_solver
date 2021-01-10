import os

from lib.lang.registry import LanguageSettings, register_language


@register_language(name="golang", extension="go")
class GolangSettings(LanguageSettings):
    LIB_PATH = os.path.join("lib", "go")

    def compile(self):
        expected_path = os.path.abspath(self.LIB_PATH)
        actual_path = os.environ.get("GOPATH") and os.path.abspath(
            os.environ.get("GOPATH")
        )
        if not actual_path or actual_path != expected_path:
            message = f"Please set GOPATH to the lib/go/ directory of this repository, e.g.\nGOPATH={expected_path}"
            raise Exception(message)
        yield f"go build -pkgdir {self.LIB_PATH} -o {self._bin_file} {self.file}"

    def solve(self):
        return os.path.join(".", self._bin_file)
