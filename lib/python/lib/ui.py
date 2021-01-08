from datetime import datetime, timedelta

CURSOR_RETURN = "\033[A\n"


class Color(object):
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    GREY = "\033[90m"
    ENDC = "\033[0m"
    UNDERLINE = "\033[4m"


class Align(object):
    LEFT = 1
    RIGHT = 2
    CENTER = 3


class Text(object):
    def __init__(self, text, color=None, underlined=False):
        self.text = text or ""
        self.color = color
        self.underlined = underlined

    @property
    def hidden_width(self):
        return len(str(self)) - len(self.text)

    def __len__(self):
        return len(self.text)

    def __repr__(self):
        string = self.text
        if self.underlined:
            string = f"{Color.UNDERLINE}{string}"
        if self.color:
            string = f"{self.color}{string}"
        if self.underlined or self.color:
            string = f"{string}{Color.ENDC}"
        return string


class Box(object):
    def __init__(self, text, width=None, align=Align.LEFT):
        self.text = text
        self.align = align
        self.width = width if width else len(text)
        self.width += text.hidden_width

    def __repr__(self):
        if self.align == Align.RIGHT:
            return str(self.text).rjust(self.width, " ")
        elif self.align == Align.CENTER:
            space = self.width - len(self.text) - self.text.hidden_width
            return (
                str(self.text)
                .rjust(self.width - space // 2, " ")
                .ljust(self.width, " ")
            )
        elif self.align == Align.LEFT:
            return str(self.text).ljust(self.width, " ")


class Spinner(object):
    CHARS = ["⣷", "⣯", "⣟", "⡿", "⢿", "⣻", "⣽", "⣾"]

    def __init__(self, refresh_rate_fps=16):
        self.active = False
        self._last_refreshed_at = None
        self._refresh_interval = timedelta(milliseconds=1000 // refresh_rate_fps)
        self._index = 0

    def start(self):
        self.active = True
        self._last_refreshed_at = datetime.now()
        self._index = 0
        return " " * 2  # One space as padding and the other as the placeholder

    def tick(self):
        now = datetime.now()
        if datetime.now() - self._last_refreshed_at >= self._refresh_interval:
            self._index = (self._index + 1) % len(self.CHARS)
            self._last_refreshed_at = now
        return f"\b{self.CHARS[self._index]}"

    def stop(self):
        self.active = False
        return "\b "


class Table(object):
    CELL_PADDING = 2

    def __init__(self, values, row_colors={}):
        self.values = values
        self.row_colors = row_colors

    def __repr__(self):
        string = ""
        for row, col, value in self._cells():
            width = self.col_widths[col]
            underlined = row == 0
            align = Align.CENTER if row == 0 else self.align(value)
            color = self.row_colors[row] if row in self.row_colors else None
            string += str(Box(Text(value, color, underlined=underlined), width, align))
            if col == len(self.values[row]) - 1:
                string += "\n"
            else:
                string += " " * self.CELL_PADDING
        return string

    def _cells(self):
        for row in range(len(self.values)):
            for col in range(len(self.values[row])):
                yield row, col, self.values[row][col]

    @staticmethod
    def align(value):
        try:
            int(value)
            return Align.RIGHT
        except:
            return Align.LEFT

    @property
    def col_widths(self):
        widths = [0 for _ in self.values[0]]
        for row in range(len(self.values)):
            for col in range(len(self.values[row])):
                if len(self.values[row][col]) > widths[col]:
                    widths[col] = len(self.values[row][col])
        return widths
