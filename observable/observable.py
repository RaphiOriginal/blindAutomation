#!/usr/bin/env python3
from abc import ABC, abstractmethod


class Observer(ABC):
    """
    The Observer interface declares the update method, used by subjects.
    """

    @abstractmethod
    def update(self, subject):
        """
        Receive update form subject
        :param subject: Subject
        """
        pass


class Subject(ABC):
    """
    The Subject interface declares a set of methods for managing subscribers.
    """

    @abstractmethod
    def attach(self, observer: Observer):
        """
        Attach an observer to subject
        :param observer: Observer
        """
        pass

    @abstractmethod
    def detach(self, observer: Observer):
        """
        Detach an observer from subject
        :param observer: Observer
        """
        pass

    @abstractmethod
    def notify(self):
        """
        Notifies all observers about an event
        """
        pass
