from lib.lang.registry import LanguageSettings, register_language


@register_language(name="python", extension="py")
class PythonSettings(LanguageSettings):
    def solve(self):
        return f"python {self.file}"
