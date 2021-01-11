import os

from dataclasses import dataclass
from typing import Tuple


class UnsupportedLanguage(Exception):
    pass


@dataclass
class LanguageSettings:
    file: str

    def compile(self):
        pass

    def solve(self):
        raise NotImplementedError(f"{type(self).__name__} must implement solve()")

    def time(self):
        return f"{self.solve()} --time"

    @property
    def _base_dir(self):
        return os.path.dirname(self.file)

    @property
    def _bin_file(self):
        return self.file.replace(".", "_")


class LanguageRegistry:
    _languages = {}
    _extensions = {}

    @classmethod
    def register(cls, name, extension, settings, timing):
        cls._languages[name] = (extension, settings, timing)
        cls._extensions[extension] = name

    @classmethod
    def all(cls):
        yield from cls._languages.keys()

    @classmethod
    def has(cls, name) -> bool:
        if name in cls._languages or name in cls._extensions:
            return True
        else:
            return False

    @classmethod
    def canonical(cls, name) -> bool:
        if name in cls._languages:
            return name
        elif name in cls._extensions:
            return cls._extensions[name]
        else:
            raise UnsupportedLanguage(name)

    @classmethod
    def get(cls, name) -> Tuple[str, LanguageSettings, bool]:
        if name in cls._languages:
            return cls._languages[name]
        else:
            raise UnsupportedLanguage(name)


def register_language(name, extension, timing=True):
    def decorator(cls):
        LanguageRegistry.register(name, extension, cls, timing)
        return cls

    return decorator
