#!/usr/bin/env python3
from abc import ABC, abstractmethod
from datetime import datetime

from sun.sundata import Sundata


class SunAPI(ABC):

    @abstractmethod
    def fetch_sundata(self, date: datetime) -> Sundata:
        """
        Collects sundata for specified date
        :param date: datetime for sundate should be fetched
        :return: sun object with all sundata
        """
        pass
