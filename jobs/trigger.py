#!/usr/bin/env python3
import logging
from datetime import datetime, time

from dateutil import tz

from jobs.job import Job
from jobs.jobmanager import JobManager
from jobs.task import Task
from shelly.shelly import Shelly
from shelly.wall import Wall
from sun.sundata import Sundata

logger = logging.getLogger(__name__)


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
    def __init__(self, sundata: Sundata, task: Task = Task.OPEN):
        super().__init__(task, sundata.get_sunrise())

    @staticmethod
    def type():
        return 'SUNRISE'

    def __repr__(self):
        return 'SunriseTrigger: { runtime: %s, task: %s }' % (self.time(), self.task())


class SunsetTrigger(Trigger):
    def __init__(self, sundata: Sundata, task: Task = Task.CLOSE):
        super().__init__(task, sundata.get_sunset())

    @staticmethod
    def type():
        return 'SUNSET'

    def __repr__(self):
        return 'SunsetTrigger: { runtime: %s, task: %s }' % (self.time(), self.task())


class SunInTrigger(Trigger):
    def __init__(self, sundata: Sundata, azimuth: int, task: Task = Task.TILT):
        super().__init__(task, sundata.find_azimuth(azimuth).time)

    @staticmethod
    def type():
        return 'SUNIN'

    def __repr__(self):
        return 'SunInTrigger: { runtime: %s, task: %s }' % (self.time(), self.task())


class SunOutTrigger(Trigger):
    def __init__(self, sundata: Sundata, azimuth: int, task: Task = Task.OPEN):
        super().__init__(task, sundata.find_azimuth(azimuth).time)

    @staticmethod
    def type():
        return 'SUNOUT'

    def __repr__(self):
        return 'SunOutTrigger: { runtime: %s, task: %s }' % (self.time(), self.task())


class TimeTrigger(Trigger):
    def __init__(self, runtime: time, task: Task):
        super().__init__(task, self.__prepare_runtime(runtime))

    def __prepare_runtime(self, runtime: time) -> datetime:
        now = datetime.now(tz.tzlocal())
        return now.replace(hour=runtime.hour, minute=runtime.minute, second=runtime.second)

    @staticmethod
    def type():
        return 'TIME'

    def __repr__(self):
        return 'TimeTrigger: { runtime: %s, task: %s }' % (self.time(), self.task())


def apply_triggers(manager: JobManager, sundata: Sundata, shelly: Shelly):
    triggers = extract_triggers(shelly.triggers, shelly.wall, sundata)
    for trigger in triggers:
        manager.add(Job(trigger, shelly))


def extract_triggers(triggerdata, wall: Wall, sundata: Sundata) -> [Trigger]:
    triggers: [Trigger] = []
    for trigger in triggerdata:
        if isinstance(trigger, str):
            if trigger == SunriseTrigger.type():
                sunrise = SunriseTrigger(sundata)
                triggers.append(sunrise)
                continue
            if trigger == SunsetTrigger.type():
                sunset = SunsetTrigger(sundata)
                triggers.append(sunset)
                continue
            if trigger == SunInTrigger.type():
                sunin = SunInTrigger(sundata, wall.in_sun())
                triggers.append(sunin)
                continue
            if trigger == SunOutTrigger.type():
                sunout = SunOutTrigger(sundata, wall.out_sun())
                triggers.append(sunout)
                continue
            logger.error('No Trigger for {} existing'.format(trigger))
            continue
        if SunriseTrigger.type() in trigger.keys():
            risetrigger = trigger.get(SunriseTrigger.type())
            task = Task.from_name(risetrigger.get('task'))
            triggers.append(SunriseTrigger(sundata, task))
            continue
        if SunsetTrigger.type() in trigger.keys():
            settrigger = trigger.get(SunsetTrigger.type())
            task = Task.from_name(settrigger.get('task'))
            triggers.append(SunsetTrigger(sundata, task))
            continue
        if SunInTrigger.type() in trigger.keys():
            intrigger = trigger.get(SunInTrigger.type())
            task = Task.from_name(intrigger.get('task'))
            triggers.append(SunInTrigger(sundata, wall.in_sun(), task))
            continue
        if SunOutTrigger.type() in trigger.keys():
            outtrigger = trigger.get(SunOutTrigger.type())
            task = Task.from_name(outtrigger.get('task'))
            triggers.append(SunOutTrigger(sundata, wall.out_sun(), task))
            continue
        if TimeTrigger.type() in trigger.keys():
            timetrigger = trigger.get(TimeTrigger.type())
            task = Task.from_name(timetrigger.get('task'))
            runtime = time.fromisoformat(timetrigger.get('time'))
            triggers.append(TimeTrigger(runtime, task))
            continue
        logger.error('No Trigger for {} existing'.format(trigger))
    return triggers
