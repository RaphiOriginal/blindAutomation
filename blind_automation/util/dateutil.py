#!/usr/bin/env python3
import datetime
from time import timezone

from dateutil.tz import tz

from ..settings import settings


class GlobalDate:
    def __init__(self, zone):
        self.__date: datetime = None
        self.__zone = zone

    def __build_date(self) -> datetime:
        now = datetime.datetime.now(self.__zone)
        return now.replace(hour=0, minute=0, second=0, microsecond=0)

    def next(self) -> datetime:
        if self.__date is None:
            self.__date = self.__build_date()
            return self.__date
        self.__date = self.__date + datetime.timedelta(days=1)
        return self.__date

    @property
    def current(self):
        return self.__date


zone: timezone = tz.gettz(settings.timezone)
date: GlobalDate = GlobalDate(zone)
