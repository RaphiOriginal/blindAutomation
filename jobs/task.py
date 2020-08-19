#!/usr/bin/env python3
import logging
from enum import Enum

from building.blind import Blind
from building.blind_state import State

logger = logging.getLogger(__name__)


class Task(Enum):
    CLOSE = 'CLOSE'
    OPEN = 'OPEN'
    TILT = 'TILT'
    HALF = 'HALF'

    @staticmethod
    def from_name(name: str):
        for _, task in Task.__members__.items():
            if task.value == name:
                return task
        raise ValueError('No matching Enum for {}'.format(name))

    def get_for(self, blind: Blind):
        if self == self.OPEN:
            return [(Open(blind),)]
        if self == self.TILT:
            return [(PreTilt(blind),), (Tilt(blind),)]
        if self == self.HALF:
            return [(PreTilt(blind),), (Half(blind),)]
        return [(Close(blind),)]


class BaseTask:
    def __init__(self, blind: Blind, target: State):
        self.blind: Blind = blind
        self.__target: State = target

    def ready(self) -> bool:
        return True

    def done(self):
        state = self.blind.stats()
        return state == self.__target

    def do(self):
        pass

    def _target(self):
        return self.__target

    def __repr__(self):
        return 'Task: {%s, %s, %s}' % (self.blind.name, self.blind.device, self.__target)


class Close(BaseTask):
    def __init__(self, blind: Blind):
        super(Close, self).__init__(blind, State.CLOSED)

    def do(self):
        return self.blind.close()


class Open(BaseTask):
    def __init__(self, blind: Blind):
        super(Open, self).__init__(blind, State.OPEN)

    def do(self):
        return self.blind.open()


class PreTilt(BaseTask):
    def __init__(self, blind: Blind):
        super(PreTilt, self).__init__(blind, State.TILT)

    def do(self):
        return self.blind.close()


class Tilt(BaseTask):
    def __init__(self, blind: Blind, degree: int = 0):
        super(Tilt, self).__init__(blind, State.TILT)
        self.__precondition: State = State.CLOSED
        self.__degree: int = degree

    def ready(self) -> bool:
        state = self.blind.stats()
        logger.debug(state)
        return state == self.__precondition or state == self._target()

    def done(self) -> bool:
        return self.blind.degree == self.__degree

    def do(self):
        return self.blind.tilt(self.__degree)


class Half(Tilt):
    def __init__(self, blind: Blind):
        super(Half, self).__init__(blind, degree=45)
