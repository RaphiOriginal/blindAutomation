#!/usr/bin/env python3
import logging
from datetime import datetime, time, timedelta

import global_date
from building.blind_interface import BlindInterface
from jobs import task
from jobs.interface import Trigger
from jobs.job import Job
from jobs.jobmanager import JobManager
from jobs.task import Task, Open, Close, Tilt
from sun.sundata import Sundata

logger = logging.getLogger(__name__)


class TriggerBase(Trigger):
    def __init__(self, task: Task, runtime: datetime):
        self._task: Task = task
        self._time: datetime = runtime
        self._offset: int = 0

    def task(self) -> Task:
        return self._task

    def set_task(self, task: Task):
        self._task = task

    def time(self) -> datetime:
        return self.__apply_offset()

    def set_offset(self, offset: int):
        self._offset = offset

    def __apply_offset(self) -> datetime:
        delta = timedelta(minutes=abs(self._offset))
        if self._offset > 0:
            return self._time + delta
        if self._offset < 0:
            return self._time - delta
        return self._time

    @staticmethod
    def create(trigger, **args) -> Trigger:
        raise NotImplementedError()

    @staticmethod
    def order() -> int:
        return 1

    def __repr__(self):
        return 'runtime: %s, task: %s, offset: %s' % (self._time, self._task, self._offset)


class SunriseTrigger(TriggerBase):
    def __init__(self, sundata: Sundata, task: Task = Open()):
        super(SunriseTrigger, self).__init__(task, sundata.get_sunrise())

    @staticmethod
    def type() -> str:
        return 'SUNRISE'

    @staticmethod
    def create(trigger, **args) -> Trigger:
        return SunriseTrigger(args.get('sundata'))

    def __repr__(self):
        return 'SunriseTrigger: { %s }' % (super(SunriseTrigger, self).__repr__())


class SunsetTrigger(TriggerBase):
    def __init__(self, sundata: Sundata, task: Task = Close()):
        super(SunsetTrigger, self).__init__(task, sundata.get_sunset())

    @staticmethod
    def type() -> str:
        return 'SUNSET'

    @staticmethod
    def create(trigger, **args) -> Trigger:
        return SunsetTrigger(args.get('sundata'))

    @staticmethod
    def order() -> int:
        return 5

    def __repr__(self):
        return 'SunsetTrigger: { %s }' % (super(SunsetTrigger, self).__repr__())


class SunInTrigger(TriggerBase):
    def __init__(self, sundata: Sundata, azimuth: int, task: Task = Tilt()):
        super(SunInTrigger, self).__init__(task, sundata.find_azimuth(azimuth).time)

    @staticmethod
    def type() -> str:
        return 'SUNIN'

    @staticmethod
    def create(trigger, **args) -> Trigger:
        return SunInTrigger(args.get('sundata'), args.get('azimuth'))

    @staticmethod
    def order() -> int:
        return 2

    def __repr__(self):
        return 'SunInTrigger: { %s }' % (super(SunInTrigger, self).__repr__())


class SunOutTrigger(TriggerBase):
    def __init__(self, sundata: Sundata, azimuth: int, task: Task = Open()):
        super(SunOutTrigger, self).__init__(task, sundata.find_azimuth(azimuth).time)

    @staticmethod
    def type() -> str:
        return 'SUNOUT'

    @staticmethod
    def create(trigger, **args) -> Trigger:
        return SunOutTrigger(args.get('sundata'), args.get('azimuth'))

    @staticmethod
    def order() -> int:
        return 3

    def __repr__(self):
        return 'SunOutTrigger: { %s }' % (super(SunOutTrigger, self).__repr__())


class TimeTrigger(TriggerBase):
    def __init__(self, runtime: time, task: Task = Close()):
        super(TimeTrigger, self).__init__(task, self.__prepare_runtime(runtime))

    @staticmethod
    def __prepare_runtime(runtime: time) -> datetime:
        return global_date.date.current.replace(hour=runtime.hour, minute=runtime.minute, second=runtime.second,
                                                microsecond=0)

    @staticmethod
    def type() -> str:
        return 'TIME'

    @staticmethod
    def create(trigger, **args) -> Trigger:
        runtime = time.fromisoformat(trigger.get('time'))
        return TimeTrigger(runtime)

    def __repr__(self):
        return 'TimeTrigger: { %s }' % (super(TimeTrigger, self).__repr__())


class AzimuthTrigger(TriggerBase):
    def __init__(self, sundata: Sundata, azimuth: int, task: Task = Close()):
        super(AzimuthTrigger, self).__init__(task, sundata.find_azimuth(azimuth).time)

    @staticmethod
    def type() -> str:
        return 'AZIMUTH'

    @staticmethod
    def create(trigger, **args) -> Trigger:
        azimuth = trigger.get('azimuth')
        return AzimuthTrigger(args.get('sundata'), azimuth)

    def __repr__(self):
        return 'AzimuthTrigger: { %s }' % (super(AzimuthTrigger, self).__repr__())


class ElevationTrigger(TriggerBase):
    def __init__(self, sundata: Sundata, elevation: int, direction: str, task: Task = Close()):
        super(ElevationTrigger, self).__init__(task, self.__pick(sundata, elevation, direction))

    @staticmethod
    def type() -> str:
        return 'ELEVATION'

    @staticmethod
    def create(trigger, **args) -> Trigger:
        elevation = trigger.get('elevation')
        direction = trigger.get('direction')
        return ElevationTrigger(args.get('sundata'), elevation, direction)

    @staticmethod
    def __pick(sundata: Sundata, elevation: int, direction: str) -> datetime:
        rising, setting = sundata.find_elevation(elevation)
        if direction == 'RISE':
            return rising.time
        return setting.time

    @staticmethod
    def order() -> int:
        return 4

    def __repr__(self):
        return 'ElevationTrigger: { %s }' % (super(ElevationTrigger, self).__repr__())


class PositionTrigger(TriggerBase):
    def __init__(self, sundata: Sundata, azimuth: int, elevation: int, direction: str, task: Task = Close()):
        super(PositionTrigger, self).__init__(task, self.__pick(sundata, azimuth, elevation, direction))

    @staticmethod
    def type() -> str:
        return 'POSITION'

    @staticmethod
    def create(trigger, **args) -> Trigger:
        azimuth = trigger.get('azimuth')
        elevation = trigger.get('elevation')
        direction = trigger.get('direction')
        return PositionTrigger(args.get('sundata'), azimuth, elevation, direction)

    @staticmethod
    def __pick(sundata: Sundata, azimuth: int, elevation: int, direction: str) -> datetime:
        azi = sundata.find_azimuth(azimuth)
        rising, setting = sundata.find_elevation(elevation)
        ele = setting
        if direction == 'RISE':
            ele = rising

        if azi.time > ele.time:
            return azi.time
        return ele.time

    def __repr__(self):
        return 'ElevationTrigger: { %s }' % (super(PositionTrigger, self).__repr__())


def apply_triggers(manager: JobManager, sundata: Sundata, blind: BlindInterface):
    triggers = extract_triggers(blind, sundata)
    logger.debug('Triggers for {}: {}'.format(blind.name, triggers))
    for trigger in triggers:
        manager.add(Job(trigger, blind))


def extract_triggers(blind: BlindInterface, sundata: Sundata) -> [Trigger]:
    triggers: [Trigger] = []
    for trigger in blind.triggers:
        if build_trigger(trigger, SunriseTrigger.type(), SunriseTrigger.create, triggers, sundata=sundata) or \
                build_trigger(trigger, SunsetTrigger.type(), SunsetTrigger.create, triggers, sundata=sundata) or \
                build_trigger(trigger, SunInTrigger.type(), SunInTrigger.create, triggers, sundata=sundata,
                              azimuth=blind.sun_in) or \
                build_trigger(trigger, SunOutTrigger.type(), SunOutTrigger.create, triggers, sundata=sundata,
                              azimuth=blind.sun_out) or \
                build_trigger(trigger, TimeTrigger.type(), TimeTrigger.create, triggers) or \
                build_trigger(trigger, AzimuthTrigger.type(), AzimuthTrigger.create, triggers, sundata=sundata) or \
                build_trigger(trigger, ElevationTrigger.type(), ElevationTrigger.create, triggers, sundata=sundata) or \
                build_trigger(trigger, PositionTrigger.type(), PositionTrigger.create, triggers, sundata=sundata):
            continue
        logger.error('No Trigger for {} existing'.format(trigger))

    sort(triggers)
    return triggers


def sort(triggers):
    triggers.sort(key=lambda t: t.order())
    triggers.sort(key=lambda t: t.time())


def build_trigger(triggerdata, type: str, constructor, triggers: [Trigger], **args) -> bool:
    logger.debug('parse: {} for {}'.format(triggers, type))
    if isinstance(triggerdata, str):
        if triggerdata == type:
            triggers.append(constructor(trigger=triggerdata, **args))
            return True
        return False
    if type in triggerdata.keys():
        triggerdict = triggerdata.get(type)
        trigger = constructor(trigger=triggerdict, **args)
        set_optionals(trigger, triggerdict)
        triggers.append(trigger)
        return True
    return False


def set_optionals(trigger, triggerdict):
    set_task(trigger, triggerdict)
    set_offset(trigger, triggerdict)


def set_task(trigger: Trigger, triggerdict):
    if 'task' in triggerdict:
        t = task.create(triggerdict.get('task'))
        if t:
            trigger.set_task(t)


def set_offset(trigger: Trigger, triggerdict):
    if 'offset' in triggerdict:
        offset = triggerdict.get('offset')
        trigger.set_offset(offset)
