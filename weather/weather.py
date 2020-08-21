#!/usr/bin/env python3
from __future__ import annotations

import logging
from abc import ABC

from weather.enum import WeatherConditionEnum, WeatherSubConditionEnum
from weather.interface import WeatherCondition

logger = logging.getLogger(__name__)


class WeatherConditionAbstract(WeatherCondition, ABC):
    def __init__(self, specific: WeatherSubConditionEnum):
        self.__specific: WeatherSubConditionEnum = specific

    @property
    def sub_condition(self) -> WeatherSubConditionEnum:
        return self.__specific

    @property
    def weather_condition(self) -> (WeatherConditionEnum, WeatherSubConditionEnum):
        return self.condition(), self.sub_condition

    def __repr__(self):
        return 'Weather: {%s, %s}' % self.weather_condition


class Storm(WeatherConditionAbstract):
    def __init__(self, code: int):
        super(Storm, self).__init__(WeatherSubConditionEnum.from_code(code))

    @staticmethod
    def applies(code: int) -> (bool, WeatherCondition):
        return code in [200, 201, 202, 210, 211, 212, 221, 230, 231, 232], Storm(code)

    @staticmethod
    def condition() -> WeatherConditionEnum:
        return WeatherConditionEnum.STORM


class Drizzle(WeatherConditionAbstract):
    def __init__(self, code: int):
        super(Drizzle, self).__init__(WeatherSubConditionEnum.from_code(code))

    @staticmethod
    def applies(code: int) -> (bool, WeatherCondition):
        return code in [300, 301, 302, 310, 311, 312, 313, 314, 321], Drizzle(code)

    @staticmethod
    def condition() -> WeatherConditionEnum:
        return WeatherConditionEnum.DRIZZLE


class Rain(WeatherConditionAbstract):
    def __init__(self, code: int):
        super(Rain, self).__init__(WeatherSubConditionEnum.from_code(code))

    @staticmethod
    def applies(code: int) -> (bool, WeatherCondition):
        return code in [500, 501, 502, 503, 504, 511, 520, 521, 522, 531], Rain(code)

    @staticmethod
    def condition() -> WeatherConditionEnum:
        return WeatherConditionEnum.RAIN


class Snow(WeatherConditionAbstract):
    def __init__(self, code: int):
        super(Snow, self).__init__(WeatherSubConditionEnum.from_code(code))

    @staticmethod
    def applies(code: int) -> (bool, WeatherCondition):
        return code in [600, 601, 602, 611, 612, 613, 615, 616, 620, 621, 622], Snow(code)

    @staticmethod
    def condition() -> WeatherConditionEnum:
        return WeatherConditionEnum.SNOW


class Atmosphere(WeatherConditionAbstract):
    def __init__(self, code: int):
        super(Atmosphere, self).__init__(WeatherSubConditionEnum.from_code(code))

    @staticmethod
    def applies(code: int) -> (bool, WeatherCondition):
        return code in [701, 711, 721, 731, 741, 751, 761, 762, 771, 781], Atmosphere(code)

    @staticmethod
    def condition() -> WeatherConditionEnum:
        return WeatherConditionEnum.ATMOSPHERE


class Clear(WeatherConditionAbstract):
    def __init__(self, code: int):
        super(Clear, self).__init__(WeatherSubConditionEnum.from_code(code))

    @staticmethod
    def applies(code: int) -> (bool, WeatherCondition):
        return code == 800, Clear(code)

    @staticmethod
    def condition() -> WeatherConditionEnum:
        return WeatherConditionEnum.CLEAR


class Clouds(WeatherConditionAbstract):
    def __init__(self, code: int):
        super(Clouds, self).__init__(WeatherSubConditionEnum.from_code(code))

    @staticmethod
    def applies(code: int) -> (bool, WeatherCondition):
        return code in range(801, 805), Clouds(code)

    @staticmethod
    def condition() -> WeatherConditionEnum:
        return WeatherConditionEnum.CLOUDS


weathers = \
    [Storm.applies, Drizzle.applies, Rain.applies, Snow.applies, Atmosphere.applies, Clear.applies, Clouds.applies]


def determine_weather_condition(code: int) -> WeatherCondition:
    for applies in weathers:
        if callable(applies) and applies(code=code)[0]:
            return applies(code=code)[1]
    raise ValueError('Code {} does not match any weather codes'.format(code))
