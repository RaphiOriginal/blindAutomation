#!/usr/bin/env python3
from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import Any, Callable

from building.interface import Shutter
from building.state import State
from event.event import Event, Blocker
from jobs import task
from jobs.task import Task, Open, Close, Tilt
from weather.enum import WeatherConditionEnum, WeatherSubConditionEnum
from weather.weather import Weather, Condition

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
        self._blocker = WeatherBlocker()

    def applies(self, trigger: Any) -> bool:
        if trigger and isinstance(trigger, Weather):
            return self.__applies(trigger.conditions)
        return False

    def __applies(self, conditions: [Condition]) -> bool:
        cond: bool = self.__cond_match(conditions)
        if self.__active:
            return not cond
        else:
            return cond

    def __cond_match(self, conditions: [Condition]) -> bool:
        for condition in conditions:
            if self._main == condition.main_condition and condition.sub_condition in self._sub:
                return True
        return False

    def set_task(self, task: Task):
        self._task = task

    def set_sub(self, intensity: [WeatherSubConditionEnum]):
        self._sub = intensity

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
    def undo(self) -> Task:
        return self._blocker.last

    @property
    def active(self) -> bool:
        return self.__active

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
    def last(self) -> Task:
        return self.__tasks.pop()

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

    def do(self, on: Shutter) -> Blocker:
        if isinstance(on, Shutter):
            if not self.active:
                self.activate()
                success = True
                for task in self._task.get(on):
                    success = task[0].do() and success
                if success:
                    self._blocker.block()
            else:
                self.deactivate()
                self._blocker.unblock()
                for task in self.undo.get(on):
                    task[0].do()
        return self._blocker

    @staticmethod
    def type() -> str:
        return 'CLOUDY'

    @staticmethod
    def create() -> WeatherEvent:
        return CloudsEvent()

    def __repr__(self):
        return 'CloudsEvent: {%s}' % super(CloudsEvent, self).__repr__()


# endregion
# region Event creation

def apply_weather_events(blind: Shutter):
    events: [Event] = []
    for event in blind.event_configs:
        if build_event(event, CloudsEvent.type(), CloudsEvent.create, events):
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
    set_task(event, eventdict)


def set_intensity(event: WeatherEvent, eventdict: dict):
    if 'intensity' in eventdict.keys():
        intensity: [WeatherSubConditionEnum] = []
        for item in eventdict['intensity']:
            intensity.append(WeatherSubConditionEnum[item])
        event.set_sub(intensity)


def set_task(event: WeatherEvent, eventdict: dict):
    if 'task' in eventdict.keys():
        t = task.create(eventdict['task'])
        if t:
            event.set_task(t)

# endregion
