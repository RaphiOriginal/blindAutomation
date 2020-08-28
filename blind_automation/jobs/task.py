#!/usr/bin/env python3
from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import Optional, Union

from ..building.interface import Shutter
from ..building.state import State
from ..event.blocker import Blocker

logger = logging.getLogger(__name__)


class Task(ABC):
    @abstractmethod
    def ready(self) -> bool:
        """
        Check if possible preconditions are met
        :return: true if precondition is met
        """
        pass

    @abstractmethod
    def done(self) -> bool:
        """
        Check if desired target is already achieved
        :return: true if target position is already met
        """
        pass

    @abstractmethod
    def do(self) -> bool:
        """
        Triggers configured command
        :return: true if command has been successful
        """
        pass

    @abstractmethod
    def get(self, blind: Shutter) -> [Task]:
        """
        Combines blinds with task necessary before calling do()
        :param blind: Blind which the task belongs to
        :return: [Task] List of Tasks to be applied in sequence
        """
        pass


def create(task: Union[str, dict]) -> Optional[Task]:
    tasks: [Task] = []
    if create_task(task, Open.type(), Open.create, tasks) or \
            create_task(task, Close.type(), Close.create, tasks) or \
            create_task(task, Tilt.type(), Tilt.create, tasks):
        return tasks[0]
    logger.error('No Task for {} existing'.format(task))
    return None


def create_task(task, type: str, constructor, tasks: [Task]) -> bool:
    if isinstance(task, str):
        if task == type:
            tasks.append(constructor())
            return True
        return False
    if type in task.keys():
        degree = task.get(type)
        tasks.append(constructor(degree=degree))
        return True
    return False


class BaseTask(Task):
    def __init__(self, blind: Optional[Shutter], target: State):
        self.blind: Shutter = blind
        self.__target: State = target

    def ready(self) -> bool:
        return True

    def done(self) -> bool:
        return False

    def do(self) -> bool:
        pass

    def get(self, blind: Shutter) -> [Task]:
        self.blind = blind
        return []

    def _target(self):
        return self.__target

    @staticmethod
    def type() -> str:
        return 'BASE'

    @staticmethod
    def create(blind: Shutter, **args) -> Task:
        raise NotImplementedError()

    def __repr__(self):
        return 'Task.%s(%s)' % (self.type(), self.blind)


class Close(BaseTask):
    def __init__(self, blind: Shutter = None):
        super(Close, self).__init__(blind, State.CLOSED)

    def done(self) -> bool:
        return self.blind.stats() == State.CLOSED

    def do(self) -> bool:
        blocker = self.blind.close()
        if blocker is not None and blocker.blocking:
            blocker.update(self)
            return False
        return True

    def get(self, blind: Shutter) -> [Task]:
        self.blind = blind
        return [Close(blind)]

    @staticmethod
    def type() -> str:
        return 'CLOSE'

    @staticmethod
    def create(**args) -> BaseTask:
        return Close()


class Open(BaseTask):
    def __init__(self, blind: Shutter = None):
        super(Open, self).__init__(blind, State.OPEN)

    def done(self) -> bool:
        return self.blind.stats() == State.OPEN

    def do(self) -> bool:
        blocker: Optional[Blocker] = self.blind.open()
        if blocker is not None and blocker.blocking:
            blocker.update(self)
            return False
        return True

    def get(self, blind: Shutter) -> [Task]:
        return [Open(blind)]

    @staticmethod
    def type() -> str:
        return 'OPEN'

    @staticmethod
    def create(**args) -> BaseTask:
        return Open()


class PreTilt(BaseTask):
    def __init__(self, blind: Shutter):
        super(PreTilt, self).__init__(blind, State.TILT)

    def done(self) -> bool:
        return self.blind.stats() == State.TILT or self.blind.stats() == State.CLOSED

    def do(self):
        blocker = self.blind.close()
        if blocker is not None and blocker.blocking:
            blocker.update(self)
            return False
        self.blind.overwrite_degree(90)
        return True

    @staticmethod
    def type() -> str:
        return 'PREPARE'

    @staticmethod
    def create(blind: Shutter, **args) -> Task:
        return Close()


class Tilt(BaseTask):
    def __init__(self, blind: Shutter = None, degree: int = 0):
        super(Tilt, self).__init__(blind, State.TILT)
        self.__precondition: State = State.CLOSED
        self.__degree: int = degree

    def ready(self) -> bool:
        state = self.blind.stats()
        logger.debug(state)
        return state == self.__precondition or state == self._target()

    def done(self) -> bool:
        return self.blind.stats() == State.TILT and self.blind.degree == self.__degree

    def do(self) -> bool:
        blocker = self.blind.tilt(self.__degree)
        if blocker is not None and blocker.blocking:
            blocker.update(self)
            return False
        return True

    def get(self, blind: Shutter) -> [Task]:
        return [PreTilt(blind), Tilt(blind, self.__degree)]

    @staticmethod
    def type() -> str:
        return 'TILT'

    @staticmethod
    def create(**args) -> BaseTask:
        if 'degree' in args:
            return Tilt(degree=args.get('degree'))
        return Tilt()

    def __repr__(self):
        return 'Task.TILT(%s)' % self.__degree
