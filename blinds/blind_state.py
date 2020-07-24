#!/usr/bin/env python3
from enum import Enum


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
        if self.__last_direction == Direction.CLOSE and self.__position == 0:
            return State.CLOSED

        if self.__last_direction == Direction.OPEN and self.__position < 5:
            return State.TILT

        return State.OPEN
