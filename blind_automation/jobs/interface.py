#!/usr/bin/env python3
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

from .task import Task


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
    def time(self) -> Optional[datetime]:
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

    @abstractmethod
    def set_days(self, on: [str]):
        """
        Sets days where the trigger only should apply
        :param on: list of days as str
        """
        pass

    @abstractmethod
    def applies(self) -> bool:
        """
        Check if this trigger can be applied at this moment
        :return: true if all conditions match
        """
        pass
