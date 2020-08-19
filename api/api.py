#!/usr/bin/env python3
import logging
from abc import ABC, abstractmethod
from datetime import datetime

from sun.sundata import Sundata
from observable.observable import Observer
from observable.observable import Subject

logger = logging.getLogger(__name__)


class SunAPI(ABC):

    @abstractmethod
    def fetch_sundata(self, date: datetime) -> Sundata:
        """
        Collects sundata for specified date
        :param date: datetime for sundate should be fetched
        :return: sun object with all sundata
        """
        pass


class ObservableSunAPI(SunAPI, Subject, ABC):
    def __init__(self):
        self._observers: [Observer] = []
        self.sundata: Sundata = None

    def attach(self, observer: Observer):
        logger.debug('Adding observer {}'.format(observer))
        self._observers.append(observer)

    def detach(self, observer: Observer):
        logger.debug('Removing observer {}'.format(observer))
        self._observers.remove(observer)

    def notify(self):
        logger.debug('Notifying observers')
        for observer in self._observers:
            observer.update(self)
