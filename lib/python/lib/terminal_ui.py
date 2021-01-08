from datetime import datetime, timedelta

CURSOR_RETURN = "\033[A\n"


class Color(object):
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    GREY = "\033[90m"


class Text(object):
    UNDERLINE = "\033[4m"
    END_FORMATTING = "\033[0m"

    def __init__(self, string, color=None, underlined=False):
        """
        Object that ties formatting information together with a string
        """
        self._string = string or ""
        self._color = color
        self._underlined = underlined

    def set_underlined(self, underlined):
        self._underlined = underlined

    @property
    def hidden_width(self):
        """
        Returns the number of characters used to format the string. When displayed in
        a terminal, the width of the string is simply the number of characters in
        self._string, however the internal representation can take up more space.
        """
        return len(str(self)) - len(self._string)

    @property
    def is_numeric(self):
        try:
            float(self._string)
            return True
        except:
            return False

    def __len__(self):
        return len(self._string)

    def __repr__(self):
        formatted = self._string
        if self._underlined:
            formatted = f"{self.UNDERLINE}{formatted}"
        if self._color:
            formatted = f"{self._color}{formatted}"
        if self._underlined or self._color:
            formatted = f"{formatted}{self.END_FORMATTING}"
        return formatted


class BoxAlign(object):
    LEFT = 1
    RIGHT = 2
    CENTER = 3


class Box(object):
    def __init__(self, text, width=None, align=BoxAlign.LEFT):
        """
        A box of set width and unit height that contains a `Text` object
        which can be aligned within the box

        :param text: a `Text` object to be displayed in the box
        :param width: character width of the box (defaults to the visible width
        of the text)
        :params align: how to align the text within the box
        """
        self.text = text
        self.align = align
        self.width = width if width else len(text)
        self.width += text.hidden_width

    def __repr__(self):
        if self.align == BoxAlign.RIGHT:
            return str(self.text).rjust(self.width, " ")
        elif self.align == BoxAlign.CENTER:
            space = self.width - len(self.text) - self.text.hidden_width
            return (
                str(self.text)
                .rjust(self.width - space // 2, " ")
                .ljust(self.width, " ")
            )
        elif self.align == BoxAlign.LEFT:
            return str(self.text).ljust(self.width, " ")


class Animation(object):
    """

    """

    def __init__(self, frames, refresh_rate_fps=16):
        self.active = False
        self._frames = frames
        self._started_at = None
        self._refresh_interval = timedelta(milliseconds=1000 // refresh_rate_fps)
        self._index = 0

    def start(self):
        self.active = True
        self._started_at = datetime.now()
        self._index = -1
        # Return a blank placeholder that will get removed after the first tick
        return " " * len(self._frames[self._index])

    def tick(self):
        clear = self.clear()
        self._index = (datetime.now() - self._started_at) // self._refresh_interval
        self._index %= len(self._frames)
        return f"{clear}{self._frames[self._index]}"

    def clear(self):
        self.active = False
        chars_to_clear = len(self._frames[self._index])
        return "\b" * chars_to_clear + " " * chars_to_clear + "\b" * chars_to_clear


class Table(object):
    def __init__(self, cells, headers=True, col_padding=2):
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

    def __repr__(self):
        string = ""
        for row, col, cell in self._each_cell():
            if self._headers and row == 0:
                cell.set_underlined(True)
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
        return string

    def _each_cell(self):
        for row in range(len(self._cells)):
            for col in range(len(self._cells[row])):
                yield row, col, self._cells[row][col]

    @property
    def _col_count(self):
        return len(self._cells[0])

    @property
    def col_widths(self):
        widths = [0 for _ in self._cells[0]]
        for row in range(len(self._cells)):
            for col in range(len(self._cells[row])):
                if len(self._cells[row][col]) > widths[col]:
                    widths[col] = len(self._cells[row][col])
        return widths
