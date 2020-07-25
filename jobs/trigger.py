from datetime import datetime, time

from jobs.task import Task
from sun.sundata import Sundata


class Trigger:
    def __init__(self, task: Task, runtime: datetime):
        self.__task: Task = task
        self.__time: datetime = runtime

    def task(self):
        return self.__task

    def time(self):
        return self.__time

    def __repr__(self):
        return 'Trigger: { runtime: %s, task: %s }' % (self.__time, self.__task)


class SunriseTrigger(Trigger):
    def __init__(self, sundata: Sundata):
        super().__init__(Task.OPEN, sundata.get_sunrise())

    def __repr__(self):
        return 'SunriseTrigger: { runtime: %s, task: %s }' % (self.time(), self.task())


class SunsetTrigger(Trigger):
    def __init__(self, sundata: Sundata):
        super().__init__(Task.CLOSE, sundata.get_sunset())

    def __repr__(self):
        return 'SunsetTrigger: { runtime: %s, task: %s }' % (self.time(), self.task())


class SunInTrigger(Trigger):
    def __init__(self, sundata: Sundata, azimuth: int):
        super().__init__(Task.TILT, sundata.find_azimuth(azimuth).time)

    def __repr__(self):
        return 'SunInTrigger: { runtime: %s, task: %s }' % (self.time(), self.task())


class SunOutTrigger(Trigger):
    def __init__(self, sundata: Sundata, azimuth: int):
        super().__init__(Task.OPEN, sundata.find_azimuth(azimuth).time)

    def __repr__(self):
        return 'SunOutTrigger: { runtime: %s, task: %s }' % (self.time(), self.task())


class TimeTrigger(Trigger):
    def __init__(self, runtime: time, task: Task):
        super().__init__(task, self.__prepare_runtime(runtime))

    def __prepare_runtime(self, runtime: time) -> datetime:
        now = datetime.now()
        now.replace(hour=runtime.hour, minute=runtime.minute, second=runtime.second)
        return now

    def __repr__(self):
        return 'TimeTrigger: { runtime: %s, task: %s }' % (self.time(), self.task())
