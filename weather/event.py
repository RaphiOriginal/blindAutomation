#!/usr/bin/env python3
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from building.interface import Shutter
from event.event import Event
from jobs.task import Task, Open
from weather.enum import WeatherConditionEnum, WeatherSubConditionEnum
from weather.weather import Weather, Condition


class WeatherEvent(Event, ABC):
    def __init__(self, task: Task, main: WeatherConditionEnum, sub=None):
        if sub is None:
            sub = []
        self._task = task
        self._main: WeatherConditionEnum = main
        self._sub: [WeatherSubConditionEnum] = sub

    def applies(self, trigger: Any) -> bool:
        if trigger and isinstance(trigger, Weather):
            return self.__cond_match(trigger.conditions)
        return False

    def __cond_match(self, conditions: [Condition]) -> bool:
        for condition in conditions:
            if self._main == condition.main_condition and condition.sub_condition in self._sub:
                return True
        return False

    def set_task(self, task: Task):
        self._task = task

    def set_sub(self, intensity: [WeatherSubConditionEnum]):
        self._sub = intensity

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
        return 'main: %s, sub: %s, task: %s' % (self._main, self._sub, self._task)


class CloudsEvent(WeatherEvent):
    def __init__(self, task: Task = Open()):
        super(CloudsEvent, self).__init__(task, WeatherConditionEnum.CLOUDS, [WeatherSubConditionEnum.OVERCAST])

    def do(self, on: Shutter) -> bool:
        if isinstance(on, Shutter):
            success: bool = True
            for task in self._task.get(on):
                success = task[0].do() and success
            return success
        return False

    @staticmethod
    def type() -> str:
        return 'CLOUDY'

    @staticmethod
    def create() -> WeatherEvent:
        return CloudsEvent()

    def __repr__(self):
        return 'CloudsEvent: {%s}' % super(CloudsEvent, self).__repr__()
