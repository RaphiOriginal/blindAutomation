#!/usr/bin/env python3
from abc import ABC, abstractmethod
from typing import List, Optional

from building.state import State
from event.event import Event, Blocker
from observable.observable import Observer


class Shutter(Observer, ABC):
    @abstractmethod
    def open(self) -> Optional[Blocker]:
        """
        Command to open blind
        :return: true if command was successful
        """
        pass

    @abstractmethod
    def close(self) -> Optional[Blocker]:
        """
        Command to close blind
        :return: true if command was successful
        """
        pass

    @abstractmethod
    def move(self, pos: int) -> Optional[Blocker]:
        """
        Command to move blind to a desired position
        :param pos: int Position the blind has move to
        :return: true if command was successful
        """
        pass

    @abstractmethod
    def tilt(self, degree: int) -> Optional[Blocker]:
        """
        Command to tilt blind to a specific degree
        :param degree: int Degre the blind has to be tilted to
        :return: true if command was successful
        """
        pass

    @abstractmethod
    def overwrite_degree(self, degree: int):
        pass

    @abstractmethod
    def stats(self) -> State:
        """
        Command to fetch blind Stat
        :return: State the blind actually has
        """
        pass

    @property
    @abstractmethod
    def id(self) -> str:
        """
        Device ID
        :return: str Device Id
        """
        pass

    @abstractmethod
    def name(self) -> str:
        """
        Name for Blind
        :return: str name
        """
        pass

    @abstractmethod
    def sun_in(self) -> float:
        """
        Azimuth degree when sun reaches blind
        :return: float azimuth
        """
        pass

    @abstractmethod
    def sun_out(self) -> float:
        """
        Azimuth degree when sun leaves blind
        :return: float azimuth
        """
        pass

    @abstractmethod
    def triggers(self) -> List:
        """
        List of triggers in string or object representation
        :return: List
        """
        pass

    @abstractmethod
    def event_configs(self) -> List:
        """
        List of event in string or object representation
        :return: List
        """
        pass

    @abstractmethod
    def degree(self) -> int:
        """
        Accesses the degree property
        :return: int degree
        """
        pass

    @abstractmethod
    def add_events(self, events: [Event]):
        """
        Adds an event trigger to its internal list
        """
        pass
