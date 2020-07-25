from datetime import datetime, time

from jobs.job import Job
from jobs.jobmanager import JobManager
from jobs.task import Task
from shelly.shelly import Shelly
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

    @staticmethod
    def type():
        return 'SUNRISE'

    def __repr__(self):
        return 'SunriseTrigger: { runtime: %s, task: %s }' % (self.time(), self.task())


class SunsetTrigger(Trigger):
    def __init__(self, sundata: Sundata):
        super().__init__(Task.CLOSE, sundata.get_sunset())

    @staticmethod
    def type():
        return 'SUNSET'

    def __repr__(self):
        return 'SunsetTrigger: { runtime: %s, task: %s }' % (self.time(), self.task())


class SunInTrigger(Trigger):
    def __init__(self, sundata: Sundata, azimuth: int):
        super().__init__(Task.TILT, sundata.find_azimuth(azimuth).time)

    @staticmethod
    def type():
        return 'SUNIN'

    def __repr__(self):
        return 'SunInTrigger: { runtime: %s, task: %s }' % (self.time(), self.task())


class SunOutTrigger(Trigger):
    def __init__(self, sundata: Sundata, azimuth: int):
        super().__init__(Task.OPEN, sundata.find_azimuth(azimuth).time)

    @staticmethod
    def type():
        return 'SUNOUT'

    def __repr__(self):
        return 'SunOutTrigger: { runtime: %s, task: %s }' % (self.time(), self.task())


class TimeTrigger(Trigger):
    def __init__(self, runtime: time, task: Task):
        super().__init__(task, self.__prepare_runtime(runtime))

    def __prepare_runtime(self, runtime: time) -> datetime:
        now = datetime.now()
        now.replace(hour=runtime.hour, minute=runtime.minute, second=runtime.second)
        return now

    @staticmethod
    def type():
        return 'TIME'

    def __repr__(self):
        return 'TimeTrigger: { runtime: %s, task: %s }' % (self.time(), self.task())


def apply_triggers(manager: JobManager, sundata: Sundata, shelly: Shelly):
    triggers = extract_triggers(shelly.triggers, sundata)
    for trigger in triggers:
        manager.add(Job(trigger, shelly))


def extract_triggers(triggerdata, sundata: Sundata) -> [Trigger]:
    triggers: [Trigger] = []
    for trigger in triggerdata:
        if trigger == SunriseTrigger.type():
            sunrise = SunriseTrigger(sundata)
            triggers.append(sunrise)
            continue
        if trigger == SunsetTrigger.type():
            sunset = SunsetTrigger(sundata)
            triggers.append(sunset)
            continue
        if trigger == SunInTrigger.type():
            sunin = SunInTrigger(sundata, 110)
            triggers.append(sunin)
            continue
        if trigger == SunOutTrigger.type():
            sunout = SunOutTrigger(sundata, 290)
            triggers.append(sunout)
            continue
        if 'task' in trigger.keys() and 'time' in trigger.keys():
            task = Task.from_name(trigger.get('task'))
            runtime = time.fromisoformat(trigger.get('time'))
            continue
        print('No Trigger for {} existing'.format(trigger))
    return triggers
