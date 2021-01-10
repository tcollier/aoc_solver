from typing import Any, Callable, Dict


class HandlerRegistry:
    _handlers = {}

    @classmethod
    def register(cls, event, func):
        cls._handlers[event] = func

    @classmethod
    def has(cls, event):
        return event in cls._handlers

    @classmethod
    def get(cls, event) -> Callable[[Any, Dict], Any]:
        return cls._handlers[event]


def register_handler(event):
    def wrapper(func):
        HandlerRegistry.register(event, func)
        return func

    return wrapper
