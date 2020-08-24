#!/usr/bin/env python3
from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Optional

import global_date
from building.interface import Shutter
from building.state import State
from event.event import Event, Blocker
from jobs import task
from jobs.task import Task, Open, Close, Tilt
from weather.enum import WeatherConditionEnum, WeatherSubConditionEnum
from weather.weather import Weather, Condition, Sun

logger = logging.getLogger(__name__)


# region Base

class WeatherEvent(Event, ABC):
    def __init__(self, task: Task, main: WeatherConditionEnum, sub=None):
        if sub is None:
            sub = []
        self._task = task
        self._main: WeatherConditionEnum = main
        self._sub: [WeatherSubConditionEnum] = sub
        self.__active: bool = False
        self._undo: Optional[Task] = None
        self._blocker = WeatherBlocker()
        self._night_mode: bool = True

    def applies(self, trigger: Any) -> bool:
        if trigger and isinstance(trigger, Weather):
            return self.__applies(trigger)
        return False

    def do(self, on: Shutter) -> Blocker:
        if isinstance(on, Shutter):
            if not self.active:
                self._set_previous(on)
                self.activate()
                success = True
                for task in self._task.get(on):
                    success = task[0].do() and success
                if success:
                    self._blocker.block()
            else:
                self.deactivate()
                self._blocker.unblock()
                if self.undo:
                    for task in self.undo.get(on):
                        task[0].do()
        return self._blocker

    def __applies(self, weather: Weather) -> bool:
        cond: bool = self.__cond_match(weather.conditions)
        if self.__active:
            return not cond or not self._allowed(weather)
        else:
            return cond and self._allowed(weather)

    def __cond_match(self, conditions: [Condition]) -> bool:
        for condition in conditions:
            if self._main == condition.main_condition and condition.sub_condition in self._sub:
                return True
        return False

    def _allowed(self, weather: Weather) -> bool:
        if self._night_mode:
            sun: Sun = weather.sun
            now: datetime = weather.time
            return sun.sunrise < now < sun.sunset
        return True

    def set_task(self, task: Task):
        self._task = task

    def set_sub(self, intensity: [WeatherSubConditionEnum]):
        self._sub = intensity

    def set_night_mode(self, night_mode: bool):
        self._night_mode = night_mode

    def _set_previous(self, blind: Shutter):
        previous = blind.stats()
        if previous == State.OPEN:
            self._undo = Open(blind)
        if previous == State.CLOSED:
            self._undo = Close(blind)
        if previous == State.TILT:
            self._undo = Tilt(blind)

    def activate(self):
        self.__active = True

    def deactivate(self):
        self.__active = False

    @property
    def undo(self) -> Optional[Task]:
        last = self._blocker.last
        if last:
            self._undo = last
        return self._undo

    @property
    def active(self) -> bool:
        return self.__active

    @property
    def blocker(self) -> Blocker:
        return self._blocker

    @staticmethod
    @abstractmethod
    def type() -> str:
        """
        Type in str format to describe itself
        :return: str Type
        """
        pass

    @staticmethod
    @abstractmethod
    def create() -> WeatherEvent:
        """
        Constructor
        :return: specific WeatherEvent
        """
        pass

    def __repr__(self):
        return 'main: %s, sub: %s, task: %s, blocker: %s' % (self._main, self._sub, self._task, self._blocker)


# endregion
# region weather blocker

class WeatherBlocker(Blocker):
    def __init__(self):
        self.__block = False
        self.__tasks: [Task] = []

    def block(self):
        self.__block = True

    def unblock(self):
        self.__block = False

    def update(self, task: Task):
        self.__tasks.append(task)

    @property
    def last(self) -> Optional[Task]:
        if len(self.__tasks) > 0:
            return self.__tasks.pop()
        return None

    @property
    def blocking(self) -> bool:
        return self.__block

    def __repr__(self):
        return 'Blocker: {blocking: %s, blocked: %s}' % (self.blocking, self.__tasks)


# endregion
# region Weather Events

class CloudsEvent(WeatherEvent):
    def __init__(self, task: Task = Open()):
        super(CloudsEvent, self).__init__(task, WeatherConditionEnum.CLOUDS, [WeatherSubConditionEnum.OVERCAST])

    @staticmethod
    def type() -> str:
        return 'CLOUDY'

    @staticmethod
    def create() -> WeatherEvent:
        return CloudsEvent()

    def __repr__(self):
        return 'CloudsEvent: {%s}' % super(CloudsEvent, self).__repr__()


class RainEvent(WeatherEvent):
    def __init__(self, task: Task = Open()):
        super(RainEvent, self).__init__(task, WeatherConditionEnum.RAIN, self.__default)

    @staticmethod
    def type() -> str:
        return 'RAIN'

    @staticmethod
    def create() -> WeatherEvent:
        return RainEvent()

    @property
    def __default(self) -> [WeatherSubConditionEnum]:
        return [WeatherSubConditionEnum.HEAVY,
                WeatherSubConditionEnum.VERY_HEAVY,
                WeatherSubConditionEnum.EXTREME,
                WeatherSubConditionEnum.SHOWER,
                WeatherSubConditionEnum.HEAVY_SHOWER,
                WeatherSubConditionEnum.RAGGED_SHOWER]

    def __repr__(self):
        return 'RainEvent: {%s}' % super(RainEvent, self).__repr__()


class ClearEvent(WeatherEvent):
    def __init__(self, task: Task = Close()):
        super(ClearEvent, self).__init__(task, WeatherConditionEnum.CLEAR, [WeatherSubConditionEnum.CLEAR])

    @staticmethod
    def type() -> str:
        return 'CLEAR'

    @staticmethod
    def create() -> WeatherEvent:
        return ClearEvent()

    def __repr__(self):
        return 'ClearEvent: {%s}' % super(ClearEvent, self).__repr__()


class StormEvent(WeatherEvent):
    def __init__(self, task: Task = Open()):
        super(StormEvent, self).__init__(task, WeatherConditionEnum.STORM, self.__default)

    @staticmethod
    def type() -> str:
        return 'STORM'

    @staticmethod
    def create() -> WeatherEvent:
        return StormEvent()

    @property
    def __default(self) -> [WeatherSubConditionEnum]:
        return [WeatherSubConditionEnum.LIGHT_RAIN,
                WeatherSubConditionEnum.RAIN,
                WeatherSubConditionEnum.HEAVY_RAIN,
                WeatherSubConditionEnum.LIGHT,
                WeatherSubConditionEnum.NORMAL,
                WeatherSubConditionEnum.HEAVY,
                WeatherSubConditionEnum.RAGGED,
                WeatherSubConditionEnum.LIGHT_DRIZZLE,
                WeatherSubConditionEnum.DRIZZLE,
                WeatherSubConditionEnum.HEAVY_DRIZZLE]

    def __repr__(self):
        return 'StormEvent: {%s}' % super(StormEvent, self).__repr__()


class DrizzleEvent(WeatherEvent):
    def __init__(self, task: Task = Open()):
        super(DrizzleEvent, self).__init__(task, WeatherConditionEnum.DRIZZLE, self.__default)

    @staticmethod
    def type() -> str:
        return 'DRIZZLE'

    @staticmethod
    def create() -> WeatherEvent:
        return DrizzleEvent()

    @property
    def __default(self) -> [WeatherSubConditionEnum]:
        return [WeatherSubConditionEnum.HEAVY_RAIN,
                WeatherSubConditionEnum.SHOWER_RAIN,
                WeatherSubConditionEnum.HEAVY_SHOWER_RAIN,
                WeatherSubConditionEnum.SHOWER]

    def __repr__(self):
        return 'DrizzleEvent: {%s}' % super(DrizzleEvent, self).__repr__()


class SnowEvent(WeatherEvent):
    def __init__(self, task: Task = Open()):
        super(SnowEvent, self).__init__(task, WeatherConditionEnum.SNOW, self.__default)

    @staticmethod
    def type() -> str:
        return 'SNOW'

    @staticmethod
    def create() -> WeatherEvent:
        return SnowEvent()

    @property
    def __default(self) -> [WeatherSubConditionEnum]:
        return [WeatherSubConditionEnum.LIGHT_RAIN,
                WeatherSubConditionEnum.RAIN,
                WeatherSubConditionEnum.LIGHT,
                WeatherSubConditionEnum.NORMAL,
                WeatherSubConditionEnum.HEAVY,
                WeatherSubConditionEnum.SHOWER,
                WeatherSubConditionEnum.LIGHT_SHOWER,
                WeatherSubConditionEnum.HEAVY_SHOWER,
                WeatherSubConditionEnum.SLEET,
                WeatherSubConditionEnum.LIGHT_SHOWER_SLEET,
                WeatherSubConditionEnum.SHOWER_SLEET]

    def __repr__(self):
        return 'SnowEvent: {%s}' % super(SnowEvent, self).__repr__()


class SpecialWeatherEvent(WeatherEvent):
    def __init__(self, task: Task = Open()):
        super(SpecialWeatherEvent, self).__init__(task, WeatherConditionEnum.ATMOSPHERE, self.__default)

    @staticmethod
    def type() -> str:
        return 'SPECIAL'

    @staticmethod
    def create() -> WeatherEvent:
        return SpecialWeatherEvent()

    @property
    def __default(self) -> [WeatherSubConditionEnum]:
        return [WeatherSubConditionEnum.MIST,
                WeatherSubConditionEnum.SMOKE,
                WeatherSubConditionEnum.HAZE,
                WeatherSubConditionEnum.WHIRLS,
                WeatherSubConditionEnum.FOG,
                WeatherSubConditionEnum.SAND,
                WeatherSubConditionEnum.DUST,
                WeatherSubConditionEnum.ASH,
                WeatherSubConditionEnum.SQUALL,
                WeatherSubConditionEnum.TORNADO]

    def __repr__(self):
        return 'SpecialWeatherEvent: {%s}' % super(SpecialWeatherEvent, self).__repr__()


# endregion
# region Event creation

def apply_weather_events(blind: Shutter):
    events: [Event] = []
    for event in blind.event_configs:
        if build_event(event, CloudsEvent.type(), CloudsEvent.create, events) or \
                build_event(event, ClearEvent.type(), ClearEvent.create, events) or \
                build_event(event, SpecialWeatherEvent.type(), SpecialWeatherEvent.create, events) or \
                build_event(event, SnowEvent.type(), SnowEvent.create, events) or \
                build_event(event, RainEvent.type(), RainEvent.create, events) or \
                build_event(event, DrizzleEvent.type(), DrizzleEvent.create, events) or \
                build_event(event, StormEvent.type(), StormEvent.create, events):
            continue
    blind.add_events(events)


def build_event(eventdata, type: str, constructor, events: [Event]) -> bool:
    logger.debug('parse: {} for {}'.format(eventdata, type))
    if isinstance(eventdata, str):
        if eventdata == type:
            events.append(constructor())
            return True
        return False
    if type in eventdata.keys():
        eventdict = eventdata.get(type)
        event = constructor()
        set_optionals(event, eventdict)
        events.append(event)
        return True
    return False


def set_optionals(event: WeatherEvent, eventdict: dict):
    set_intensity(event, eventdict)
    set_events(event, eventdict)
    set_task(event, eventdict)
    set_night_mode(event, eventdict)


def set_intensity(event: WeatherEvent, eventdict: dict):
    if 'intensity' in eventdict.keys():
        intensity: [WeatherSubConditionEnum] = []
        for item in eventdict['intensity']:
            intensity.append(WeatherSubConditionEnum[item])
        event.set_sub(intensity)


def set_events(event: WeatherEvent, eventdict: dict):
    if 'events' in eventdict.keys():
        intensity: [WeatherSubConditionEnum] = []
        for item in eventdict['events']:
            intensity.append(WeatherSubConditionEnum[item])
        event.set_sub(intensity)


def set_task(event: WeatherEvent, eventdict: dict):
    if 'task' in eventdict.keys():
        t = task.create(eventdict['task'])
        if t:
            event.set_task(t)


def set_night_mode(event: WeatherEvent, evendict: dict):
    if 'night' in evendict.keys():
        night_mode = evendict['night']
        event.set_night_mode(night_mode)

# endregion