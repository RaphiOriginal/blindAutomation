#!/usr/bin/env python3
from building.blind_state import fetch_blindstate, BlindState
from building.state import State
from device.device import Device


class Shelly(Device):

    def __init__(self, id: str):
        self.__id: str = id

    @property
    def id(self):
        return self.__id

    def get_status(self):
        return '{}/status'.format(self.url)

    def stats(self) -> State:
        return self._fetch_stats('{}/roller/0'.format(self.url))

    def move(self, pos: int) -> bool:
        return self._send('{}/roller/0?go=to_pos&roller_pos={}'.format(self.url, pos))

    def tilt(self, direction: str, time: float) -> bool:
        return self._send('{}/roller/0?go={}&duration={}'.format(self.url, direction, time))

    def open(self) -> bool:
        return self._send('{}/roller/0?go=open'.format(self.url))

    def close(self) -> bool:
        return self._send('{}/roller/0?go=close'.format(self.url))

    def __repr__(self):
        return 'Shelly: { id: %s, ip: %s}' % (self.__id, self.url)
