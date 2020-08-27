from typing import Optional, TypeVar

from blind_automation.event.event import EventBlocker

T = TypeVar('T')


class Blocker(EventBlocker):
    def __init__(self):
        self.__block = False
        self.__block_list: [T] = []

    def block(self):
        self.__block = True

    def unblock(self):
        self.__block = False

    def update(self, task: T):
        self.__block_list.append(task)

    @property
    def last(self) -> Optional[T]:
        if len(self.__block_list) > 0:
            return self.__block_list.pop()
        return None

    @property
    def blocking(self) -> bool:
        return self.__block

    def __repr__(self):
        return 'Blocker: {blocking: %s, blocked: %s}' % (self.blocking, self.__block_list)
