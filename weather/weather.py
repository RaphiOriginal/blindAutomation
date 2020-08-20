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


class Drizzle(Weather):
    @staticmethod
    def applies(code: int) -> (bool, Weather):
        return code in [300, 301, 302, 310, 311, 312, 313, 314, 321], Drizzle()

    @staticmethod
    def type() -> WeatherType:
        return WeatherType.DRIZZLE


class Rain(Weather):
    @staticmethod
    def applies(code: int) -> (bool, Weather):
        return code in [500, 501, 502, 503, 504, 511, 520, 521, 522, 531], Rain()

    @staticmethod
    def type() -> WeatherType:
        return WeatherType.RAIN


class Snow(Weather):
    @staticmethod
    def applies(code: int) -> (bool, Weather):
        return code in [600, 601, 602, 611, 612, 613, 615, 616, 620, 621, 622], Snow()

    @staticmethod
    def type() -> WeatherType:
        return WeatherType.SNOW


class Atmosphere(Weather):
    @staticmethod
    def applies(code: int) -> (bool, Weather):
        return code in [701, 711, 721, 731, 741, 751, 761, 762, 771, 781], Atmosphere()

    @staticmethod
    def type() -> WeatherType:
        return WeatherType.ATMOSPHERE


class Clear(Weather):
    @staticmethod
    def applies(code: int) -> (bool, Weather):
        return code == 800, Clear()

    @staticmethod
    def type() -> WeatherType:
        return WeatherType.CLEAR


class Clouds(Weather):
    @staticmethod
    def applies(code: int) -> (bool, Weather):
        return code in range(801, 805), Clouds()

    @staticmethod
    def type() -> WeatherType:
        return WeatherType.CLOUDS


weathers = \
    [Storm.applies, Drizzle.applies, Rain.applies, Snow.applies, Atmosphere.applies, Clear.applies, Clouds.applies]


def determine_weather(code: int) -> Weather:
    for applies in weathers:
        if callable(applies) and applies(code=code)[0]:
            return applies(code=code)[1]
    raise ValueError('Code {} does not match any weather codes'.format(code))
