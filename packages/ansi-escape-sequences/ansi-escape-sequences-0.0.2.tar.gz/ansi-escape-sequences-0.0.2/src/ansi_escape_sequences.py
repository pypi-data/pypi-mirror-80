# https://en.wikipedia.org/wiki/ANSI_escape_code
CSI = '\033['
OSC = '\033]'
BEL = '\007'


def set_title(title):
    return OSC + '2;' + title + BEL


class Cursor(object):
    def Up(self, n=1):
        return CSI + str(n) + 'A'

    def Down(self, n=1):
        return CSI + str(n) + 'B'

    def Forward(self, n=1):
        return CSI + str(n) + 'C'

    def Back(self, n=1):
        return CSI + str(n) + 'D'

    def NextLine(self, n=1):
        return CSI + str(n) + 'E'

    def PreviousLine(self, n=1):
        return CSI + str(n) + 'F'

    def HorizontalAbsolute(self, n=1):
        return CSI + str(n) + 'G'

    def Position(self, x=1, y=1):
        return CSI + str(y) + ';' + str(x) + 'H'

    def HorizontalVerticalPosition(self, x=1, y=1):
        return CSI + str(x) + ';' + str(y) + 'f'

    def SaveCurrentPosition(self):
        return CSI + 's'

    def RestoreSavedPosition(self):
        return CSI + 'u'

    def Show(self):
        return CSI + "?25h"

    def Hide(self):
        return CSI + "?25l"


class Erase(object):
    def Display(self, mode=2):
        return CSI + str(mode) + 'J'

    def Line(self, mode=2):
        return CSI + str(mode) + 'K'


class Scroll(object):
    def Up(self, n=1):
        return CSI + str(n) + 'S'

    def Down(self, n=1):
        return CSI + str(n) + 'T'


class AUXPort(object):
    def On(self):
        return CSI + "5i"

    def Off(self):
        return CSI + "4i"


class ScreenBuffer(object):
    def Enable(self):
        return CSI + "?1049h"

    def Disable(self):
        return CSI + "?1049l"


class Bracketed(object):
    def On(self):
        return CSI + "?2004h"

    def Off(self):
        return CSI + "?2004l"


# https://en.wikipedia.org/wiki/ANSI_escape_code#3/4_bit
def bit3_4(n=0, m=0):
    return CSI + str(n) + ';' + str(m) + 'm'


# https://en.wikipedia.org/wiki/ANSI_escape_code#8-bit
def bit8(n=0):
    return ";5;" + str(n)


# https://en.wikipedia.org/wiki/ANSI_escape_code#24-bit
def bit24(r=0, g=0, b=0):
    return ";2;" + str(r) + ';' + str(g) + ';' + str(b)


def foregroundbit8(n=0):
    return CSI + str(38) + bit8(n) + 'm'


def backgroundbit8(n=0):
    return CSI + str(48) + bit8(n) + 'm'


def foregroundbit24(r=0, g=0, b=0):
    return CSI + str(38) + bit24(r, g, b) + 'm'


def backgroundbit24(r=0, g=0, b=0):
    return CSI + str(48) + bit24(r, g, b) + 'm'


# https://en.wikipedia.org/wiki/ANSI_escape_code#SGR_parameters
def reset():
    return CSI + 'm'


class SGRList(object):
    def __init__(self):
        for name in dir(self):
            if not name.startswith('_'):
                value = getattr(self, name)
                setattr(self, name, CSI + str(value) + 'm')


class Intensity(SGRList):
    INCREASED = 1
    DECREASED = 2
    NORMAL = 22


class Italic(SGRList):
    ON = 3
    OFF = 23


class Underline(SGRList):
    ON = 4
    DOUBLY = 21
    OFF = 24
    DEFAULT_COLOR = 59


class Blink(SGRList):
    SLOW = 5
    RAPID = 6
    NORMAL = 25


class Reverse(SGRList):
    ON = 7
    OFF = 27


class Conceal(SGRList):
    ON = 8
    NORMAL = 28


class CrossedOut(SGRList):
    ON = 9
    OFF = 29


class Font(SGRList):
    DEFAULT = 10
    FONT_1 = 11
    FONT_2 = 12
    FONT_3 = 13
    FONT_4 = 14
    FONT_5 = 15
    FONT_6 = 16
    FONT_7 = 17
    FONT_8 = 18
    FONT_9 = 19


class Fraktur(SGRList):
    ON = 20
    OFF = 23


class ProportionalSpacing(SGRList):
    ON = 26
    OFF = 50


class Foreground(SGRList):
    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    MAGENTA = 35
    CYAN = 36
    WHITE = 37
    DEFAULT = 39


class Background(SGRList):
    BLACK = 40
    RED = 41
    GREEN = 42
    YELLOW = 43
    BLUE = 45
    MAGENTA = 46
    CYAN = 47
    WHITE = 48
    DEFAULT = 49


class Encircled(SGRList):
    ON = 52
    OFF = 54


class Framed(SGRList):
    ON = 51
    OFF = 54


class Overlined(SGRList):
    ON = 53
    OFF = 55


class Ideogram(SGRList):
    UNDERLINE_OR_RIGHT_SIDE_LINE = 60
    DOUBLE_UNDERLINE_OR_DOUBLE_LINE_ON_THE_RIGHT_SIDE = 61
    OVERLINE_OR_LEFT_SIDE_LINE = 62
    DOUBLE_OVERLINE_OR_DOUBLE_LINE_ON_THE_LEFT_SIDE = 63
    STRESS_MARKING = 64
    OFF = 65


class Script(SGRList):
    SUPER = 73
    SUB = 74


class BrightForeground(SGRList):
    BLACK = 90
    RED = 91
    GREEN = 92
    YELLOW = 93
    BLUE = 94
    MAGENTA = 95
    CYAN = 96
    WHITE = 97


class BrightBackground(SGRList):
    BLACK = 100
    RED = 101
    GREEN = 102
    YELLOW = 103
    BLUE = 104
    MAGENTA = 105
    CYAN = 106
    WHITE = 107
