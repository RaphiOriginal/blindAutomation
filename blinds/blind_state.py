#!/usr/bin/env python3
from enum import Enum

import requests


class Direction(Enum):
    OPEN = 'open'
    CLOSE = 'close'

    @classmethod
    def from_name(cls, name: str):
        for _, direction in Direction.__members__.items():
            if direction.value == name:
                return direction
        raise ValueError('No matching Enum for {}'.format(name))


class State(Enum):
    OPEN = 1
    CLOSED = 2
    TILT = 3


class BlindState:
    def __init__(self, position: int, direction: Direction):
        self.__position: int = position
        self.__last_direction: Direction = direction

    def __int__(self, position: int, direction: str):
        self.__position: int = position
        self.__last_direction: Direction = Direction.from_name(direction)

    def state(self):
        if self.__last_direction == Direction.CLOSE.value and self.__position == 0:
            return State.CLOSED

        if self.__last_direction == Direction.OPEN.value and self.__position < 5:
            return State.TILT

        return State.OPEN

    def __repr__(self):
        return 'BlindState: { position: %s, last_direction: %s, state: %s}' %\
               (self.__position, self.__last_direction, self.state())


def fetch_blindstate(shelly):
    response = requests.get(shelly.get_roller())
    if response.status_code == 200:
        data = response.json()
        return BlindState(data.get('current_pos'), data.get('last_direction'))
    raise ConnectionError('Negative answer from shelly {}: {} - {}'
                          .format(shelly.id, response.status_code, response.text))