#!/usr/bin/env python3
from __future__ import annotations

import logging

from weather.enum import WeatherConditionEnum, WeatherSubConditionEnum
from weather.interface import WeatherCondition

logger = logging.getLogger(__name__)


class Condition(WeatherCondition):
    def __init__(self, code: int, description: str = 'Keine', icon: str = '01d'):
        self.__condition: WeatherConditionEnum = WeatherConditionEnum.from_code(code)
        self.__sub_condition: WeatherSubConditionEnum = WeatherSubConditionEnum.from_code(code)
        self.__description: str = description
        self.__icon: str = icon

    @property
    def main_condition(self) -> WeatherConditionEnum:
        return self.__condition

    @property
    def sub_condition(self) -> WeatherSubConditionEnum:
        return self.__sub_condition

    @property
    def condition(self) -> (WeatherConditionEnum, WeatherSubConditionEnum):
        return self.__condition, self.__sub_condition

    @property
    def description(self) -> str:
        return self.__description

    @property
    def icon(self) -> str:
        return self.__icon

    def __repr__(self):
        return 'Weather: {main: %s, sub: %s, description: %s, icon: %s}' % \
               (self.main_condition, self.sub_condition, self.description, self.icon)


class Temperature:
    def __init__(self, data: dict):
        self.__data: dict = data
        self.__temp: float = 0.0
        self.__feels_like: float = 0.0
        self.__temp_min: float = 0.0
        self.__temp_max: float = 0.0
        self.__parse_temperature()

    @property
    def temp(self) -> float:
        return self.__temp

    @property
    def feels_like(self) -> float:
        return self.__feels_like

    @property
    def temp_min(self) -> float:
        return self.__temp_min

    @property
    def temp_max(self) -> float:
        return self.__temp_max

    def __parse_temperature(self):
        self.__temp = self.__data.get('temp')
        self.__feels_like = self.__data.get('feels_like')
        self.__temp_min = self.__data.get('temp_min')
        self.__temp_max = self.__data.get('temp_max')

    def __repr__(self):
        return 'Temperature: {temp: %s, feels_like: %s, temp_min: %s, temp_max: %s}' % \
               (self.temp, self.feels_like, self.temp_min, self.temp_max)


class Atmosphere:
    def __init__(self, data: dict):
        self.__data: dict = data
        self.__pressure: int = 0
        self.__humidity: int = 0
        self.__parse_atmosphere()

    @property
    def pressure(self) -> int:
        return self.__pressure

    @property
    def humidity(self) -> int:
        return self.__humidity

    def __parse_atmosphere(self):
        self.__pressure = self.__data.get('pressure')
        self.__humidity = self.__data.get('humidity')

    def __repr__(self):
        return 'Atmosphere: {pressure: %s, humidity: %s}' % (self.pressure, self.humidity)


class Wind:
    def __init__(self, data: dict):
        self.__data: dict = data
        self.__speed: float = 0.0
        self.__deg: int = 0
        self.__parse_wind()

    @property
    def speed(self) -> float:
        return self.__speed

    @property
    def deg(self) -> int:
        return self.__deg

    def __parse_wind(self):
        self.__speed = self.__data.get('speed')
        self.__deg = self.__data.get('deg')

    def __repr__(self):
        return 'Wind: {speed: %s, deg: %s}' % (self.speed, self.deg)


class Clouds:
    def __init__(self, data: dict):
        self.__data: dict = data
        self.__all: int = 0
        self.__parse_clouds()

    @property
    def all(self) -> int:
        return self.__all

    def __parse_clouds(self):
        self.__all = self.__data.get('all')

    def __repr__(self):
        return 'Clouds: {all: %s}' % self.all


class Weather:
    def __init__(self, data: dict):
        self.__data: dict = data
        self.__conditions: [Condition] = []
        self.__temperature: Temperature = Temperature(data.get('main'))
        self.__atmosphere: Atmosphere = Atmosphere(data.get('main'))
        self.__wind: Wind = Wind(data.get('wind'))
        self.__clouds: Clouds = Clouds(data.get('clouds'))
        self.__parse_weather()

    @property
    def conditions(self) -> [Condition]:
        return self.__conditions

    @property
    def temperature(self) -> Temperature:
        return self.__temperature

    @property
    def atmosphere(self) -> Atmosphere:
        return self.__atmosphere

    @property
    def wind(self) -> Wind:
        return self.__wind

    @property
    def clouds(self) -> Clouds:
        return self.__clouds

    def __parse_weather(self):
        weather_list = self.__data.get('weather')
        for weather in weather_list:
            code = weather.get('id')
            self.__conditions.append(Condition(code, weather.get('description'), weather.get('icon')))

    def __repr__(self):
        return 'Weather: {%s, %s, %s, %s, %s}' % \
               (self.conditions, self.temperature, self.atmosphere, self.wind, self.clouds)
