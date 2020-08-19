#!/usr/bin/env python3
import logging

from building.blind import Blind
from building.blind_state import State

logger = logging.getLogger(__name__)


class Task:
    def ready(self) -> bool:
        pass

    def done(self):
        pass

    def do(self):
        pass

    def get(self, blind: Blind) -> [__name__]:
        pass


def create(task) -> Task:
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

    def get(self, blind: Blind) -> [Task]:
        self.blind = blind
        return []

    def _target(self):
        return self.__target

    @staticmethod
    def type() -> str:
        return 'BASE'

    @staticmethod
    def create(blind: Blind, **args) -> Task:
        raise NotImplementedError()

    def __repr__(self):
        return 'Task.%s' % self.type()


class Close(BaseTask):
    def __init__(self, blind: Blind = None):
        super(Close, self).__init__(blind, State.CLOSED)

    def do(self):
        return self.blind.close()

    def get(self, blind: Blind) -> [Task]:
        self.blind = blind
        return [(self,)]

    @staticmethod
    def type() -> str:
        return 'CLOSE'

    @staticmethod
    def create(**args) -> BaseTask:
        return Close()


class Open(BaseTask):
    def __init__(self, blind: Blind = None):
        super(Open, self).__init__(blind, State.OPEN)

    def do(self):
        return self.blind.open()

    def get(self, blind: Blind) -> [Task]:
        self.blind = blind
        return [(self,)]

    @staticmethod
    def type() -> str:
        return 'OPEN'

    @staticmethod
    def create(**args) -> BaseTask:
        return Open()


class PreTilt(BaseTask):
    def __init__(self, blind: Blind):
        super(PreTilt, self).__init__(blind, State.TILT)

    def do(self):
        return self.blind.close()

    @staticmethod
    def type() -> str:
        return 'PREPARE'


class Tilt(BaseTask):
    def __init__(self, blind: Blind = None, degree: int = 0):
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

    def get(self, blind: Blind) -> [Task]:
        self.blind = blind
        return [(PreTilt(self.blind),), (self,)]

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


OPEN = Open()
CLOSE = Close()
TILT = Tilt()
