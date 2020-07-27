#!/usr/bin/env python3
import logging
from enum import Enum

from blinds import blind_state
from blinds.blind_state import State
from shelly.shelly import Shelly


logger = logging.getLogger(__name__)


class Task(Enum):
    CLOSE = 'CLOSE'
    OPEN = 'OPEN'
    TILT = 'TILT'

    @staticmethod
    def from_name(name: str):
        for _, task in Task.__members__.items():
            if task.value == name:
                return task
        raise ValueError('No matching Enum for {}'.format(name))

    def get_for(self, shelly: Shelly):
        if self == self.OPEN:
            return [(Open(shelly),)]
        if self == self.TILT:
            return [(PreTilt(shelly),), (Tilt(shelly),)]
        return [(Close(shelly),)]


class BaseTask:
    def __init__(self, shelly: Shelly, target: State, position: int):
        self.shelly: Shelly = shelly
        self.__target: State = target
        self.__position: int = position

    def ready(self):
        return True

    def done(self):
        state = blind_state.fetch_blindstate(self.shelly)
        return state.state() == self.__target

    def do(self):
        return self.shelly.set_roller(self.__position)


class Close(BaseTask):
    def __init__(self, shelly: Shelly):
        super().__init__(shelly, State.CLOSED, 0)


class Open(BaseTask):
    def __init__(self, shelly: Shelly):
        super().__init__(shelly, State.OPEN, 100)


class PreTilt(BaseTask):
    def __init__(self, shelly: Shelly):
        super().__init__(shelly, State.TILT, 0)


class Tilt(BaseTask):
    def __init__(self, shelly: Shelly):
        super().__init__(shelly, State.TILT, 2)
        self.__precondition: State = State.CLOSED

    def ready(self):
        state = blind_state.fetch_blindstate(self.shelly)
        logger.debug(state)
        return state.state() == self.__precondition
