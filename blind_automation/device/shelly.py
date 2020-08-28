#!/usr/bin/env python3
from ..building.state import State
from .device import Device


class Shelly(Device):

    def __init__(self, id: str):
        self.__id: str = id

    @property
    def id(self) -> str:
        return self.__id

    def stats(self) -> State:
        return self._fetch_stats('roller/0')

    def move(self, pos: int) -> bool:
        return self._send('roller/0?go=to_pos&roller_pos={}'.format(pos))

    def tilt(self, direction: str, time: float) -> bool:
        return self._send('roller/0?go={}&duration={}'.format(direction, time))

    def open(self) -> bool:
        return self._send('roller/0?go=open')

    def close(self) -> bool:
        return self._send('roller/0?go=close')

    def __repr__(self):
        return 'Shelly: { id: %s, ip: %s}' % (self.__id, self.url)
