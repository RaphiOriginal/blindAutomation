#!/usr/bin/env python3
from __future__ import annotations

from abc import ABC, abstractmethod

from weather.enum import WeatherConditionEnum, WeatherSubConditionEnum


class WeatherCondition(ABC):

    @staticmethod
    @abstractmethod
    def applies(code: int) -> (bool, WeatherCondition):
        """
        Returns true if code matches one of the class codes and returns class
        :param code: int Weather code
        :return: Tuple bool and Weather
        """
        pass

    @staticmethod
    @abstractmethod
    def condition() -> WeatherConditionEnum:
        """
        Returns WeatherType that is represented by Class
        :return: WeatherType
        """
        pass

    @property
    @abstractmethod
    def sub_condition(self) -> WeatherSubConditionEnum:
        """
        Returns
        :return:
        """
        pass

    @property
    @abstractmethod
    def weather_condition(self) -> (WeatherConditionEnum, WeatherSubConditionEnum):
        """
        Returns touple with main condition and sub condition
        :return: (WeatherConditionEnum, WeatherSupConditionEnum)
        """
        pass
