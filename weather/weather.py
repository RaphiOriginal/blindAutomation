#!/usr/bin/env python3
from __future__ import annotations
from abc import ABC, abstractmethod
from enum import Enum
from typing import Callable


class WeatherType(Enum):
    STORM = 1
    DRIZZLE = 2
    RAIN = 3
    SNOW = 4
    MIST = 5
    SMOKE = 6
    HAZE = 7
    DUST = 8
    ASH = 9
    SQUALL = 10
    TORNADO = 11
    CLEAR = 12
    CLOUDS = 13
    ATMOSPHERE = 14


class Weather(ABC):
    @staticmethod
    @abstractmethod
    def applies(code: int) -> (bool, Weather):
        """
        Returns true if code matches one of the class codes and returns class
        :param code: int Weather code
        :return: Tuple bool and Weather
        """
        pass

    @staticmethod
    @abstractmethod
    def type() -> WeatherType:
        """
        Returns WeatherType that is represented by Class
        :return: WeatherType
        """
        pass


class Storm(Weather):
    @staticmethod
    def applies(code: int) -> (bool, Weather):
        return code in [200, 201, 202, 210, 211, 212, 221, 230, 231, 232], Storm()

    @staticmethod
    def type() -> WeatherType:
        return WeatherType.STORM

    class StormEnum(Enum):
        LIGHT_RAIN = 200
        RAIN = 201
        HEAVY_RAIN = 202
        LIGHT = 210
        NORMAL = 211
        HEAVY = 212
        RAGGED = 221
        LIGHT_DRIZZLE = 230
        DRIZZLE = 231
        HEAVY_DRIZZLE = 232


class Drizzle(Weather):
    @staticmethod
    def applies(code: int) -> (bool, Weather):
        return code in [300, 301, 302, 310, 311, 312, 313, 314, 321], Drizzle()

    @staticmethod
    def type() -> WeatherType:
        return WeatherType.DRIZZLE

    class DrizzleEnum(Enum):
        LIGHT = 300
        NORMAL = 301
        HEAVY = 302
        LIGHT_RAIN = 310
        RAIN = 311
        HEAVY_RAIN = 312
        SHOWER_RAIN = 313
        HEAVY_SHOWER_RAIN = 314
        SHOWER = 321


class Rain(Weather):
    @staticmethod
    def applies(code: int) -> (bool, Weather):
        return code in [500, 501, 502, 503, 504, 511, 520, 521, 522, 531], Rain()

    @staticmethod
    def type() -> WeatherType:
        return WeatherType.RAIN

    class RainEnum(Enum):
        LIGHT = 500
        MODERATE = 501
        HEAVY = 502
        VERY_HEAVY = 503
        EXTREME = 504
        FREEZING = 511
        LIGHT_SHOWER = 520
        SHOWER = 521
        HEAVY_SHOWER = 522
        RAGGED_SHOWER = 531


class Snow(Weather):
    @staticmethod
    def applies(code: int) -> (bool, Weather):
        return code in [600, 601, 602, 611, 612, 613, 615, 616, 620, 621, 622], Snow()

    @staticmethod
    def type() -> WeatherType:
        return WeatherType.SNOW

    class SnowEnum(Enum):
        LIGHT = 600
        NORMAL = 601
        HEAVY = 602
        SLEET = 611
        LIGHT_SHOWER_SLEET = 612
        SHOWER_SLEET = 613
        LIGHT_RAIN = 615
        RAIN = 616
        LIGHT_SHOWER = 620
        SHOWER = 621
        HEAVY_SHOWER = 622


class Atmosphere(Weather):
    @staticmethod
    def applies(code: int) -> (bool, Weather):
        return code in [701, 711, 721, 731, 741, 751, 761, 762, 771, 781], Atmosphere()

    @staticmethod
    def type() -> WeatherType:
        return WeatherType.ATMOSPHERE

    class AtmosphereEnum(Enum):
        MIST = 701
        SMOKE = 711
        HAZE = 721
        WHIRLS = 731
        FOG = 741
        SAND = 751
        DUST = 761
        ASH = 762
        SQUALL = 771
        TORNADO = 781


class Clear(Weather):
    @staticmethod
    def applies(code: int) -> (bool, Weather):
        return code == 800, Clear()

    @staticmethod
    def type() -> WeatherType:
        return WeatherType.CLEAR

    class ClearEnum(Enum):
        CLEAR = 800


class Clouds(Weather):
    @staticmethod
    def applies(code: int) -> (bool, Weather):
        return code in range(801, 805), Clouds()

    @staticmethod
    def type() -> WeatherType:
        return WeatherType.CLOUDS

    class CloudsEnum(Enum):
        FEW = 801  # 11-25%
        SCATTERED = 802  # 25-50%
        BROKEN = 803  # 51-84%
        OVERCAST = 804  # 85-100%


weathers = \
    [Storm.applies, Drizzle.applies, Rain.applies, Snow.applies, Atmosphere.applies, Clear.applies, Clouds.applies]


def determine_weather(code: int) -> Weather:
    for applies in weathers:
        if callable(applies) and applies(code=code)[0]:
            return applies(code=code)[1]
    raise ValueError('Code {} does not match any weather codes'.format(code))
