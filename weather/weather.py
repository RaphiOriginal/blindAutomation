#!/usr/bin/env python3
from __future__ import annotations

import logging

from weather.enum import WeatherConditionEnum, WeatherSubConditionEnum
from weather.interface import WeatherCondition

logger = logging.getLogger(__name__)


class Condition(WeatherCondition):
    def __init__(self, code: int):
        self.__condition: WeatherConditionEnum = WeatherConditionEnum.from_code(code)
        self.__sub_condition: WeatherSubConditionEnum = WeatherSubConditionEnum.from_code(code)

    @property
    def main_condition(self) -> WeatherConditionEnum:
        return self.__condition

    @property
    def sub_condition(self) -> WeatherSubConditionEnum:
        return self.__sub_condition

    @property
    def condition(self) -> (WeatherConditionEnum, WeatherSubConditionEnum):
        return self.__condition, self.__sub_condition

    def __repr__(self):
        return 'Weather: {%s, %s}' % self.condition
