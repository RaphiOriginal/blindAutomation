from enum import Enum


class State(Enum):
    OPEN = 1
    CLOSED = 2
    TILT = 3
    MOVED = 4
    UNKNOWN = 5
