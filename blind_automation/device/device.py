#!/usr/bin/env python3
import logging
from abc import ABC, abstractmethod
from enum import Enum

import requests

from ..building.blind.state import fetch_blindstate
from ..building.state import State

logger = logging.getLogger(__name__)


class Device(ABC):
    url: str = None
    __active: bool = False
    __queue: [str] = []

    @abstractmethod
    def close(self) -> bool:
        """
        Command to close blind
        :return: true if command has been send
        """
        pass

    @abstractmethod
    def open(self) -> bool:
        """
        Command to open blind
        :return: true if command has been send
        """
        pass

    @abstractmethod
    def move(self, pos: int) -> bool:
        """
        Command to move blinds to a specific percentage
        :param pos: desired blind position in percentage
        :return: true if command has been send
        """
        pass

    @abstractmethod
    def tilt(self, direction: str, time: float) -> bool:
        """
        Command to move blinds in a specific direction for a specific time
        :param direction: str direction to move
        :param time: time in seconds how long the blinds should move
        :return: true if command has been send
        """
        pass

    @abstractmethod
    def stats(self) -> State:
        """
        Status Request for device
        :return: State which represents the position of the device
        """
        pass

    def activate(self):
        logger.info('Activating: {}'.format(self))
        self.__active = True
        if len(self.__queue) > 0:
            self._send(self.__queue.pop())
            self.__queue = []

    def deactivate(self):
        logger.info('Deactivating: {}'.format(self))
        self.__active = False

    @property
    def active(self) -> bool:
        return self.__active

    def _send(self, path) -> bool:
        url = '{}/{}'.format(self.url, path)
        if not self.__active:
            logger.info('Device not active')
            self.__queue.append(path)
            return False
        order = requests.get(url)
        if order.status_code != 200:
            logger.error('Call {} failed with status {} and content: {}'.format(url, order.status_code, order.text))
            return False
        else:
            logger.info('Task {} send: {}'.format(url, order.text))
            return True

    def _fetch_stats(self, path: str) -> State:
        if not self.active:
            return State.UNKNOWN
        return fetch_blindstate('{}/{}'.format(self.url, path)).state()

    @abstractmethod
    def id(self) -> str:
        """
        (Readonly) Device Id
        :return: str Device Id
        """
        pass


class Typ(Enum):
    SHELLY = 1
