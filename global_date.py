import datetime

from dateutil.tz import tz


def build_date() -> datetime:
    now = datetime.datetime.now(tz.tzlocal())
    return now.replace(hour=0, minute=0, second=0, microsecond=0)


date: datetime = build_date()
