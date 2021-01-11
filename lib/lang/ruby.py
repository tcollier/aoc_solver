from lib.lang.registry import LanguageSettings, register_language


@register_language(name="ruby", extension="rb")
class RubySettings(LanguageSettings):
    def solve(self):
        return f"ruby {self.file}"
