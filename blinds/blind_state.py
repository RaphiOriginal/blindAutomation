#!/usr/bin/env python3
from enum import Enum

import requests

from blinds.blind import Blind
from blinds.state import State


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

        if self.__last_direction == Direction.OPEN and self.__position < 5:
            return State.TILT

        return State.OPEN

    def __repr__(self):
        return 'BlindState: { position: %s, last_direction: %s, state: %s}' %\
               (self.__position, self.__last_direction, self.state())


def fetch_blindstate(blind: Blind):
    response = requests.get(blind.stats())
    if response.status_code == 200:
        data = response.json()
        blind.state = BlindState(data.get('current_pos'), data.get('last_direction'))
        return blind.state
    raise ConnectionError('Negative answer from shelly {}: {} - {}'
                          .format(blind.id, response.status_code, response.text))
