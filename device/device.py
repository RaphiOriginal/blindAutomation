import logging
from enum import Enum

import requests

from building.blind_state import fetch_blindstate
from building.state import State

logger = logging.getLogger(__name__)


class Device:
    url: str = None
    __active = False

    def close(self) -> bool:
        pass

    def open(self) -> bool:
        pass

    def move(self, pos: int) -> bool:
        pass

    def stats(self) -> State:
        pass

    def activate(self):
        logger.info('Activating: {}'.format(self))
        self.__active = True

    def deactivate(self):
        logger.info('Deactivating: {}'.format(self))
        self.__active = False

    @property
    def active(self) -> bool:
        return self.__active

    def _send(self, url) -> bool:
        if not self.__active:
            logger.info('Device not active')
            return False
        order = requests.get(url)
        if order.status_code != 200:
            logger.error('Call with {} failed with status {} and content: {}'.format(url, order.status_code, order.text))
            return False
        else:
            logger.info('Task {} send: {}'.format(url, order.text))
            return True

    def _fetch_stats(self, url: str) -> State:
        if not self.active:
            return State.UNKNOWN
        return fetch_blindstate(url).state()

    @property
    def id(self):
        pass


class Typ(Enum):
    SHELLY = 1