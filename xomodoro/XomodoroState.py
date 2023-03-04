import enum


class XomodoroState(enum.Enum):
    focus = enum.auto()
    long_break = enum.auto()
    short_break = enum.auto()
    stopped = enum.auto()
