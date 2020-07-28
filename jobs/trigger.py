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
    def task(self) -> Task:
        pass

    def set_task(self):
        pass

    def time(self):
        pass


class TriggerBase(Trigger):
    def __init__(self, task: Task, runtime: datetime):
        self.__task: Task = task
        self.__time: datetime = runtime

    def task(self) -> Task:
        return self.__task

    def set_task(self, task: Task):
        self.__task = task

    def time(self) -> datetime:
        return self.__time

    @staticmethod
    def create(trigger, **args) -> Trigger:
        raise NotImplementedError()

    def __repr__(self):
        return 'Trigger: { runtime: %s, task: %s }' % (self.__time, self.__task)


class SunriseTrigger(TriggerBase):
    def __init__(self, sundata: Sundata, task: Task = Task.OPEN):
        super().__init__(task, sundata.get_sunrise())

    @staticmethod
    def type() -> str:
        return 'SUNRISE'

    @staticmethod
    def create(trigger, **args) -> Trigger:
        return SunriseTrigger(args.get('sundata'))

    def __repr__(self):
        return 'SunriseTrigger: { runtime: %s, task: %s }' % (self.time(), self.task())


class SunsetTrigger(TriggerBase):
    def __init__(self, sundata: Sundata, task: Task = Task.CLOSE):
        super().__init__(task, sundata.get_sunset())

    @staticmethod
    def type() -> str:
        return 'SUNSET'

    @staticmethod
    def create(trigger, **args) -> Trigger:
        return SunsetTrigger(args.get('sundata'))

    def __repr__(self):
        return 'SunsetTrigger: { runtime: %s, task: %s }' % (self.time(), self.task())


class SunInTrigger(TriggerBase):
    def __init__(self, sundata: Sundata, azimuth: int, task: Task = Task.TILT):
        super().__init__(task, sundata.find_azimuth(azimuth).time)

    @staticmethod
    def type() -> str:
        return 'SUNIN'

    @staticmethod
    def create(trigger, **args) -> Trigger:
        return SunInTrigger(args.get('sundata'), args.get('azimuth'))

    def __repr__(self):
        return 'SunInTrigger: { runtime: %s, task: %s }' % (self.time(), self.task())


class SunOutTrigger(TriggerBase):
    def __init__(self, sundata: Sundata, azimuth: int, task: Task = Task.OPEN):
        super().__init__(task, sundata.find_azimuth(azimuth).time)

    @staticmethod
    def type() -> str:
        return 'SUNOUT'

    @staticmethod
    def create(trigger, **args) -> Trigger:
        return SunOutTrigger(args.get('sundata'), args.get('azimuth'))

    def __repr__(self):
        return 'SunOutTrigger: { runtime: %s, task: %s }' % (self.time(), self.task())


class TimeTrigger(TriggerBase):
    def __init__(self, runtime: time, task: Task = Task.CLOSE):
        super().__init__(task, self.__prepare_runtime(runtime))

    def __prepare_runtime(self, runtime: time) -> datetime:
        now = datetime.now(tz.tzlocal())
        return now.replace(hour=runtime.hour, minute=runtime.minute, second=runtime.second, microsecond=0)

    @staticmethod
    def type() -> str:
        return 'TIME'

    @staticmethod
    def create(trigger, **args) -> Trigger:
        runtime = time.fromisoformat(trigger.get('time'))
        return TimeTrigger(runtime)

    def __repr__(self):
        return 'TimeTrigger: { runtime: %s, task: %s }' % (self.time(), self.task())


def apply_triggers(manager: JobManager, sundata: Sundata, shelly: Shelly):
    triggers = extract_triggers(shelly.triggers, shelly.wall, sundata)
    for trigger in triggers:
        manager.add(Job(trigger, shelly))


def extract_triggers(triggerdata, wall: Wall, sundata: Sundata) -> [Trigger]:
    triggers: [Trigger] = []
    for trigger in triggerdata:
        if build_trigger(trigger, SunriseTrigger.type(), SunriseTrigger.create, triggers, sundata=sundata):
            continue
        if build_trigger(trigger, SunsetTrigger.type(), SunsetTrigger.create, triggers, sundata=sundata):
            continue
        if build_trigger(trigger, SunInTrigger.type(), SunInTrigger.create, triggers, sundata=sundata, azimuth=wall.in_sun()):
            continue
        if build_trigger(trigger, SunOutTrigger.type(), SunOutTrigger.create, triggers, sundata=sundata, azimuth=wall.out_sun()):
            continue
        if build_trigger(trigger, TimeTrigger.type(), TimeTrigger.create, triggers):
            continue
        logger.error('No Trigger for {} existing'.format(trigger))
    return triggers


def build_trigger(triggerdata, type: str, constructor, triggers: [Trigger], **args) -> bool:
    if isinstance(triggerdata, str):
        if triggerdata == type:
            triggers.append(constructor(trigger=triggerdata, **args))
            return True
        return False
    if type in triggerdata.keys():
        triggerdict = triggerdata.get(type)
        task = Task.from_name(triggerdict.get('task'))
        trigger = constructor(trigger=triggerdict, **args)
        trigger.set_task(task)
        triggers.append(trigger)
        return True
    return False
