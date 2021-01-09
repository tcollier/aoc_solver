from datetime import datetime, timedelta
from enum import Enum
from typing import Generator, List, Set

from lib.typing import Stringable


class Element(Stringable):
    pass


class TextColor:
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    GREY = "\033[90m"


class TextFormat:
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


class Text(Element):
    END_FORMATTING = "\033[0m"

    def __init__(
        self, string: str, color: TextColor = None, formats: Set[TextFormat] = None
    ):
        """
        Object that ties formatting information together with a string
        """
        self._string = string or ""
        self._color = color
        self._formats = formats if formats else set()

    def add_format(self, format: TextFormat):
        self._formats.add(format)

    @property
    def hidden_width(self) -> int:
        """
        Returns the number of characters used to format the string. When displayed in
        a terminal, the width of the string is simply the number of characters in
        self._string, however the internal representation can take up more space.
        """
        return len(str(self)) - len(self._string)

    @property
    def is_numeric(self) -> bool:
        try:
            float(self._string)
            return True
        except:
            return False

    def __len__(self):
        return len(self._string)

    def __repr__(self):
        formatted = self._string
        for format in self._formats:
            formatted = f"{format}{formatted}"
        if self._color:
            formatted = f"{self._color}{formatted}"
        if self._formats or self._color:
            formatted = f"{formatted}{self.END_FORMATTING}"
        return formatted


CURSOR_RETURN = Text("\033[A\n")


class BoxAlign(Enum):
    LEFT = 1
    RIGHT = 2
    CENTER = 3


class BoxDisplay(Enum):
    INLINE = 0
    BLOCK = 1


class Box(Element):
    def __init__(
        self,
        text: Text,
        width: int = None,
        align: BoxAlign = BoxAlign.LEFT,
        display: BoxDisplay = BoxDisplay.INLINE,
    ):
        """
        A box of set width and unit height that contains a `Text` object
        which can be aligned within the box

        :param text: a `Text` object to be displayed in the box
        :param width: character width of the box (defaults to the visible width
        of the text)
        :params align: how to align the text within the box
        """
        self._text = text
        self._align = align
        self._display = display
        self._width = width if width else len(text)
        self._width += text.hidden_width

    def __repr__(self):
        string = str(self._text)
        if self._align == BoxAlign.RIGHT:
            string = string.rjust(self._width, " ")
        elif self._align == BoxAlign.CENTER:
            space = self._width - len(self._text) - self._text.hidden_width
            string = string.rjust(self._width - space // 2, " ").ljust(self._width, " ")
        elif self._align == BoxAlign.LEFT:
            string = string.ljust(self._width, " ")
        if self._display == BoxDisplay.BLOCK:
            string += "\n"
        return string


class Animation:
    """
    Animate the frames (a list of strings) at the given refresh rate. The `tick`
    function will clear any previously drawn characters.
    """

    active = False
    _started_at = None
    _index = -1

    def __init__(self, frames: List[str], refresh_rate_fps: int = 16):
        self._frames = frames
        self._refresh_interval = timedelta(milliseconds=1000 // refresh_rate_fps)

    def start(self) -> str:
        self._started_at = datetime.now()
        self._index = -1
        self.active = True
        # Return a blank placeholder that will get removed after the first tick
        return Text(" " * len(self._frames[self._index]))

    def tick(self) -> str:
        clear = self._erase_previous()
        self._index = (datetime.now() - self._started_at) // self._refresh_interval
        self._index %= len(self._frames)
        return Text(f"{clear}{self._frames[self._index]}")

    def clear(self) -> str:
        self.active = False
        return Text(self._erase_previous())

    def _erase_previous(self) -> str:
        chars_to_clear = len(self._frames[self._index])
        return "\b" * chars_to_clear + " " * chars_to_clear + "\b" * chars_to_clear


class Table(Element):
    def __init__(
        self,
        cells: List[List[Element]],
        headers: bool = True,
        col_padding: int = 2,
        display: BoxDisplay = BoxDisplay.BLOCK,
    ):
        """
        Display a table of Text objects

        :param cells: 2 dimensional list of `Text` objects to be displayed in
        table format
        :param headers: True if the first row is to be formatted as the column
        headers
        :params col_padding: number of empty spaces to add between each column
        """
        self._cells = cells
        self._headers = headers
        self._col_padding = col_padding
        self._display = display

    def __repr__(self):
        string = ""
        for row, col, cell in self._each_cell():
            if self._headers and row == 0:
                cell.add_format(TextFormat.UNDERLINE)
                align = BoxAlign.CENTER
            elif cell.is_numeric:
                align = BoxAlign.RIGHT
            else:
                align = BoxAlign.LEFT
            string += str(Box(cell, self.col_widths[col], align))
            if col == self._col_count - 1:
                string += "\n"
            else:
                string += " " * self._col_padding
        return string + ("\n" if self._display == BoxDisplay.BLOCK else "")

    def _each_cell(self) -> Generator[int, int, Element]:
        for row in range(len(self._cells)):
            for col in range(len(self._cells[row])):
                yield row, col, self._cells[row][col]

    @property
    def _col_count(self) -> int:
        return len(self._cells[0])

    @property
    def col_widths(self) -> List[int]:
        widths = [0 for _ in self._cells[0]]
        for row in range(len(self._cells)):
            for col in range(len(self._cells[row])):
                if len(self._cells[row][col]) > widths[col]:
                    widths[col] = len(self._cells[row][col])
        return widths
