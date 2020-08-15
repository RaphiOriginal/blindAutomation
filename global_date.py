import datetime

from dateutil.tz import tz


class GlobalDate:
    __date: datetime = None

    @staticmethod
    def build_date() -> datetime:
        now = datetime.datetime.now(tz.tzlocal())
        return now.replace(hour=0, minute=0, second=0, microsecond=0)

    def next(self) -> datetime:
        if self.__date is None:
            self.__date = self.build_date()
            return self.__date
        self.__date = self.__date + datetime.timedelta(days=1)
        return self.__date

    @property
    def date(self):
        return self.__date


date: GlobalDate = GlobalDate()
