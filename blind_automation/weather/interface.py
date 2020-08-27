#!/usr/bin/env python3
from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

from .enum import WeatherConditionEnum, WeatherSubConditionEnum


class ConditionData(ABC):

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


class TemperatureData(ABC):

    @property
    @abstractmethod
    def temp(self) -> float:
        """
        Temperature
        :return: temperature
        """
        pass

    @property
    @abstractmethod
    def feels_like(self) -> float:
        """
        Feels like temperature
        :return: temperature
        """
        pass

    @property
    @abstractmethod
    def temp_min(self) -> float:
        """
        Min temperature
        :return: temperature
        """
        pass

    @property
    @abstractmethod
    def temp_max(self) -> float:
        """
        Max temperature
        :return: temperature
        """
        pass


class AtmosphereData(ABC):

    @property
    @abstractmethod
    def pressure(self) -> int:
        """
        Air pressure
        :return: pressure
        """
        pass

    @property
    @abstractmethod
    def humidity(self) -> int:
        """
        Air humidity
        :return: humidity
        """
        pass


class WindData(ABC):

    @property
    @abstractmethod
    def speed(self) -> float:
        """
        Wind speed
        :return: speed
        """
        pass

    @property
    @abstractmethod
    def deg(self) -> int:
        """
        Wind direction in degrees
        :return: direction
        """
        pass


class CloudsData(ABC):

    @property
    @abstractmethod
    def all(self) -> int:
        """
        Cloud coverate in percentage
        :return: all
        """
        pass


class SunData(ABC):

    @property
    @abstractmethod
    def sunrise(self) -> datetime:
        """
        Datetime when the sun rises
        :return: datetime
        """
        pass

    @property
    @abstractmethod
    def sunset(self) -> datetime:
        """
        Datetime when the sun sets
        :return: datetime
        """
        pass


class WeatherData(ABC):

    @property
    @abstractmethod
    def conditions(self) -> [ConditionData]:
        """
        Weather condition with main and sub condition
        :return: ConditionData
        """
        pass

    @property
    @abstractmethod
    def temperature(self) -> TemperatureData:
        """
        Temperature object with temperature data
        :return: TemperatureData
        """
        pass

    @property
    @abstractmethod
    def atmosphere(self) -> AtmosphereData:
        """
        Atmosphere object with air data
        :return: AtmosphereData
        """
        pass

    @property
    @abstractmethod
    def wind(self) -> WindData:
        """
        Wind object with wind data
        :return: WindData
        """
        pass

    @property
    @abstractmethod
    def clouds(self) -> CloudsData:
        """
        Clouds object with cloud data
        :return: CloudsData
        """
        pass

    @property
    @abstractmethod
    def sun(self) -> SunData:
        """
        Sun object with sunrise and sunset date
        :return: SunData
        """
        pass

    @property
    @abstractmethod
    def time(self) -> datetime:
        """
        Timestamp when the current weather data applies
        :return: datetime
        """
        pass


class WeatherAPI(ABC):

    @abstractmethod
    def fetch_current(self) -> Optional[WeatherData]:
        """
        Fetches and returns current weather
        :return: Optional WeatherData
        """