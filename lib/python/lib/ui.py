class Color(object):
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    GREY = "\033[90m"
    ENDC = "\033[0m"
    UNDERLINE = "\033[4m"


class Decimal(object):
    def __init__(self, number):
        self.number = number

    def __repr__(self):
        return "{:.2f}".format(self.number)


class Align(object):
    LEFT = 1
    RIGHT = 2
    CENTER = 3


class TermText(object):
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

    def __init__(self):
        self.ticker = 0
        self.active = False

    def start(self):
        self.ticker = 0
        self.active = True
        return " " * 2  # One space as padding and the other as the placeholder

    def tick(self):
        self.ticker += 1
        self.index = self.ticker // 2 % len(self.CHARS)
        return f"\b{self.CHARS[self.index]}"

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
        for row in range(len(self.values)):
            for col in range(len(self.values[row])):
                if row == 0:
                    string += str(
                        Box(
                            TermText(self.values[row][col], underlined=True),
                            self.col_widths[col],
                            Align.CENTER,
                        )
                    )
                else:
                    string += str(
                        Box(
                            TermText(self.values[row][col], self.row_colors[row]),
                            self.col_widths[col],
                            self.align(self.values[row][col]),
                        )
                    )
                string += (
                    (" " * self.CELL_PADDING) if col < len(self.values[row]) - 1 else ""
                )
            string += "\n"
        return string

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
