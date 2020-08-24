#!/usr/bin/env python3
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, TypeVar, Generic


class Event(ABC):

    @abstractmethod
    def applies(self, trigger: Any) -> bool:
        """
        Check if the Event applies. Always typecheck the trigger it could by anything!
        :param trigger: object that could trigger an event
        :return: True if event applies
        """
        pass

    @abstractmethod
    def do(self, on: Any) -> bool:
        """
        Execute the event
        :param on: Blinds to be moved
        :return: True if event was Successfully executed
        """
        pass

    @property
    @abstractmethod
    def active(self) -> bool:
        """
        Returns true if event is active
        :return: True if event is active
        """
        pass


T = TypeVar('T')


class EventBlocker(ABC):

    @abstractmethod
    def block(self):
        """
        Will let the Blocker be blocking
        """
        pass

    @abstractmethod
    def unblock(self):
        """
        Will release Blocker from blocking
        """
        pass

    @abstractmethod
    def update(self, blocked: T):
        """
        Will tell the Blocker which task has been blocked, in case the task has to be applied after the blocking
        :param blocked: Blocked Task
        """
        pass

    @property
    @abstractmethod
    def last(self) -> T:
        """
        Returns last blocked task
        :return: last blocked Task
        """
        pass

    @property
    @abstractmethod
    def blocking(self) -> bool:
        """
        To check if Blocker is blocking
        :return: true if Blocker should block
        """
        pass
