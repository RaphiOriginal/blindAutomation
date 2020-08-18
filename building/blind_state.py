#!/usr/bin/env python3
from enum import Enum

import requests

from building.state import State


class Direction(Enum):
    OPEN = 'open'
    CLOSE = 'close'

    @classmethod
    def from_name(cls, name: str):
        for _, direction in Direction.__members__.items():
            if direction.value == name:
                return direction
        raise ValueError('No matching Enum for {}'.format(name))


class BlindState:
    def __init__(self, position: int, direction):
        self.__position: int = position
        if isinstance(direction, Direction):
            self.__last_direction: Direction = direction
        else:
            self.__last_direction: Direction = Direction.from_name(direction)

    def state(self):
        if self.__last_direction == Direction.CLOSE and self.__position == 0:
            return State.CLOSED

        if self.__last_direction == Direction.OPEN and 2 <= self.__position <= 5:
            return State.TILT

        if self.__last_direction == Direction.OPEN and self.__position == 1:
            return State.HALF

        return State.OPEN

    def __repr__(self):
        return 'BlindState: { position: %s, last_direction: %s, state: %s}' %\
               (self.__position, self.__last_direction, self.state())


def fetch_blindstate(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return BlindState(data.get('current_pos'), data.get('last_direction'))
    raise ConnectionError('Negative answer from deviceurl {}: {} - {}'
                          .format(url, response.status_code, response.text))
