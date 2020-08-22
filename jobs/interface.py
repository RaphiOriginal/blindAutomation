from abc import ABC, abstractmethod
from datetime import datetime

from jobs.task import Task


class PriorityManager(ABC):
    @abstractmethod
    def prio(self, runtime: datetime) -> int:
        """
        manages prio to avoid collitions on runtime
        :param runtime: datetime
        :return: int
        """


class Trigger(ABC):
    @abstractmethod
    def task(self) -> Task:
        """
        Returns configured Task
        :return: Task
        """
        pass

    @abstractmethod
    def set_task(self, task: Task):
        """
        Sets Task for the trigger
        :param task: Task
        """
        pass

    @abstractmethod
    def time(self):
        """
        Returns time where the Task needs to be triggered. Time will be caluclated with defined time and offset
        :return: datetime of configured time + offset
        """
        pass

    @abstractmethod
    def set_offset(self, offset: int):
        """
        Sets offset in minutes which will be used to calculate trigger time
        :param offset:
        """
        pass