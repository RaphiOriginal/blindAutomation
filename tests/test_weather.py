#!/usr/bin/env python3
import json
import unittest

from weather.enum import WeatherSubConditionEnum
from weather.weather import WeatherConditionEnum, Condition, Weather, Temperature, Atmosphere, Wind, Clouds


class WeatherConditionTestCase(unittest.TestCase):
    def test_clear(self):
        w = Condition(800)
        self.assertEqual(WeatherConditionEnum.CLEAR, w.main_condition)
        self.assertEqual(WeatherSubConditionEnum.CLEAR, w.sub_condition)

    def test_clouds(self):
        for code in [801, 802, 803, 804]:
            w = Condition(code)
            self.assertEqual(WeatherConditionEnum.CLOUDS, w.main_condition)
        w = Condition(804)
        self.assertEqual(WeatherSubConditionEnum.OVERCAST, w.sub_condition)

    def test_atmosphere(self):
        for code in [701, 711, 721, 731, 741, 751, 761, 762, 771, 781]:
            w = Condition(code)
            self.assertEqual(WeatherConditionEnum.ATMOSPHERE, w.main_condition)
        w = Condition(781)
        self.assertEqual(WeatherSubConditionEnum.TORNADO, w.sub_condition)

    def test_snow(self):
        for code in [600, 601, 602, 611, 612, 613, 615, 616, 620, 621, 622]:
            w = Condition(code)
            self.assertEqual(WeatherConditionEnum.SNOW, w.main_condition)
        w = Condition(601)
        self.assertEqual(WeatherSubConditionEnum.NORMAL, w.sub_condition)

    def test_rain(self):
        for code in [500, 501, 502, 503, 504, 511, 520, 521, 522, 531]:
            w = Condition(code)
            self.assertEqual(WeatherConditionEnum.RAIN, w.main_condition)
        w = Condition(501)
        self.assertEqual(WeatherSubConditionEnum.MODERATE, w.sub_condition)

    def test_drizzle(self):
        for code in [300, 301, 302, 310, 311, 312, 313, 314, 321]:
            w = Condition(code)
            self.assertEqual(WeatherConditionEnum.DRIZZLE, w.main_condition)
        w = Condition(301)
        self.assertEqual(WeatherSubConditionEnum.NORMAL, w.sub_condition)

    def test_storm(self):
        for code in [200, 201, 202, 210, 211, 212, 221, 230, 231, 232]:
            w = Condition(code)
            self.assertEqual(WeatherConditionEnum.STORM, w.main_condition)
        w = Condition(221)
        self.assertEqual(WeatherSubConditionEnum.RAGGED, w.sub_condition)

    def test_fallback(self):
        w = Condition(999)
        self.assertEqual((WeatherConditionEnum.UNKNOWN, WeatherSubConditionEnum.UNKNOWN), w.condition)

    def test_weather(self):
        w = Condition(781)
        self.assertEqual((WeatherConditionEnum.ATMOSPHERE, WeatherSubConditionEnum.TORNADO), w.condition)


class WeatherTestCase(unittest.TestCase):
    def test_parsing(self):
        mock = get_json()
        w = Weather(mock)
        cond = w.conditions
        temp = w.temperature
        atmos = w.atmosphere
        wind = w.wind
        clouds = w.clouds
        self.assertEqual(1, len(cond))
        self.__check_condition(cond[0], WeatherConditionEnum.CLEAR, WeatherSubConditionEnum.CLEAR, 'Klarer Himmel', '01d')
        self.__check_temperature(temp, 29.85, 31.87, 28.89, 31.11)
        self.__check_atmosphere(atmos, 1011, 49)
        self.__check_wind(wind, 1.09, 165)
        self.__check_clouds(clouds, 0)

    def __check_condition(self, condition: Condition, main: WeatherConditionEnum, sub: WeatherSubConditionEnum,
                          description: str, icon: str):
        self.assertIsNotNone(condition)
        self.assertEqual(main, condition.main_condition)
        self.assertEqual(sub, condition.sub_condition)
        self.assertEqual(description, condition.description)
        self.assertEqual(icon, condition.icon)

    def __check_temperature(self, temperature: Temperature, temp: float, feels_like: float, temp_min: float, temp_max: float):
        self.assertIsNotNone(temperature)
        self.assertEqual(temp, temperature.temp)
        self.assertEqual(feels_like, temperature.feels_like)
        self.assertEqual(temp_min, temperature.temp_min)
        self.assertEqual(temp_max, temperature.temp_max)

    def __check_atmosphere(self, atmosphere: Atmosphere, pressure: int, humidity: int):
        self.assertIsNotNone(atmosphere)
        self.assertEqual(pressure, atmosphere.pressure)
        self.assertEqual(humidity, atmosphere.humidity)

    def __check_wind(self, wind: Wind, speed: float, deg: int):
        self.assertIsNotNone(wind)
        self.assertEqual(speed, wind.speed)
        self.assertEqual(deg, wind.deg)

    def __check_clouds(self, clouds: Clouds, all: int):
        self.assertIsNotNone(clouds)
        self.assertEqual(all, clouds.all)


def get_json():
    with open('tests/mock/weather.json', 'r') as stream:
        return json.loads(stream.read())


if __name__ == '__main__':
    unittest.main()
