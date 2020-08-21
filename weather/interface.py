#!/usr/bin/env python3
from __future__ import annotations

from abc import ABC, abstractmethod

from weather.enum import WeatherConditionEnum, WeatherSubConditionEnum


class WeatherCondition(ABC):

    @property
    @abstractmethod
    def main_condition(self) -> WeatherConditionEnum:
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
    def condition(self) -> (WeatherConditionEnum, WeatherSubConditionEnum):
        """
        Returns touple with main condition and sub condition
        :return: (WeatherConditionEnum, WeatherSupConditionEnum)
        """
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """
        Returns description
        :return: str
        """
        pass

    @property
    @abstractmethod
    def icon(self) -> str:
        """
        Returns icon
        :return: str
        """
        pass
