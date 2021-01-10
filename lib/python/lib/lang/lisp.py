from lib.lang.registry import LanguageSettings, register_language


@register_language(name="lisp", extension="lisp", timing=False)
class ListSettings(LanguageSettings):
    def solve(self):
        return f"sbcl --script {self.file}"
