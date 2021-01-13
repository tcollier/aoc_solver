from typing import Any, Callable, Dict, Iterator

from aoc_solver.types import StringableIterator

HandlerFunc = Callable[[Any, Dict], StringableIterator]


class HandlerRegistry:
    _handlers = {}

    @classmethod
    def register(cls, event: str, func: HandlerFunc):
        cls._handlers[event] = func

    @classmethod
    def has(cls, event: str):
        return event in cls._handlers

    @classmethod
    def get(cls, event: str) -> HandlerFunc:
        return cls._handlers[event]


def register_handler(event: str):
    def wrapper(func: HandlerFunc):
        HandlerRegistry.register(event, func)
        return func

    return wrapper
