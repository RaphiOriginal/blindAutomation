from enum import Enum


class Device:
    url: str = None

    def close(self):
        pass

    def open(self):
        pass

    def move(self, pos: int):
        pass

    def stats(self):
        pass

    @property
    def id(self):
        pass


class Typ(Enum):
    SHELLY = 1