from dataclasses import dataclass
from functools import wraps
from typing import Generator, List, Tuple, Union

from lib.terminal import handlers
from lib.terminal.elements import (
    Animation,
    Box,
    BoxDisplay,
    TextColor,
    Text,
)
from lib.terminal.registry import HandlerRegistry
from lib.typing import PipeMessage, TextDisplayableHandler

SPINNER_CHARS = ["⣷", "⣯", "⣟", "⡿", "⢿", "⣻", "⣽", "⣾"]


class MessagePriority:
    LOW = 2
    MEDIUM = 1
    HIGH = 0


class Display:
    _instance = None

    def __init__(self):
        self.default_priority = MessagePriority.MEDIUM
        self._spinner = Animation(SPINNER_CHARS)
        self._handlers = {}

    def handle(self, message: PipeMessage) -> TextDisplayableHandler:
        event = message["event"]
        handler = (
            HandlerRegistry.get(event)
            if HandlerRegistry.has(event)
            else self._invalid_command
        )
        yield from handler(self, message)

    def tick(self) -> TextDisplayableHandler:
        if self._spinner.active:
            yield (self._spinner.tick(), MessagePriority.LOW)

    def set_busy(self, busy) -> TextDisplayableHandler:
        if busy and not self._spinner.active:
            yield (" ", MessagePriority.LOW)
            yield (self._spinner.start(), MessagePriority.LOW)
        elif not busy and self._spinner.active:
            yield (self._spinner.clear(), MessagePriority.HIGH)

    def _invalid_command(_self, cmd: str, args: PipeMessage) -> TextDisplayableHandler:
        yield Box(
            Text(f"Invalid command {cmd} with arguments {args}", TextColor.RED),
            display=BoxDisplay.BLOCK,
        )
