import unittest

from weather import weather
from weather.enum import WeatherSubConditionEnum
from weather.weather import Clear, Clouds, Atmosphere, Snow, Rain, Drizzle, Storm, WeatherConditionEnum


class WeatherTestCase(unittest.TestCase):
    def test_clear(self):
        w = weather.determine_weather_condition(800)
        self.assertEqual(Clear.condition(), w.condition())
        self.assertEqual(WeatherSubConditionEnum.CLEAR, w.sub_condition)

    def test_clouds(self):
        for code in [801, 802, 803, 804]:
            w = weather.determine_weather_condition(code)
            self.assertEqual(Clouds.condition(), w.condition())
        w = weather.determine_weather_condition(804)
        self.assertEqual(WeatherSubConditionEnum.OVERCAST, w.sub_condition)

    def test_atmosphere(self):
        for code in [701, 711, 721, 731, 741, 751, 761, 762, 771, 781]:
            w = weather.determine_weather_condition(code)
            self.assertEqual(Atmosphere.condition(), w.condition())
        w = weather.determine_weather_condition(781)
        self.assertEqual(WeatherSubConditionEnum.TORNADO, w.sub_condition)

    def test_snow(self):
        for code in [600, 601, 602, 611, 612, 613, 615, 616, 620, 621, 622]:
            w = weather.determine_weather_condition(code)
            self.assertEqual(Snow.condition(), w.condition())
        w = weather.determine_weather_condition(601)
        self.assertEqual(WeatherSubConditionEnum.NORMAL, w.sub_condition)

    def test_rain(self):
        for code in [500, 501, 502, 503, 504, 511, 520, 521, 522, 531]:
            w = weather.determine_weather_condition(code)
            self.assertEqual(Rain.condition(), w.condition())
        w = weather.determine_weather_condition(501)
        self.assertEqual(WeatherSubConditionEnum.MODERATE, w.sub_condition)

    def test_drizzle(self):
        for code in [300, 301, 302, 310, 311, 312, 313, 314, 321]:
            w = weather.determine_weather_condition(code)
            self.assertEqual(Drizzle.condition(), w.condition())
        w = weather.determine_weather_condition(301)
        self.assertEqual(WeatherSubConditionEnum.NORMAL, w.sub_condition)

    def test_storm(self):
        for code in [200, 201, 202, 210, 211, 212, 221, 230, 231, 232]:
            w = weather.determine_weather_condition(code)
            self.assertEqual(Storm.condition(), w.condition())
        w = weather.determine_weather_condition(221)
        self.assertEqual(WeatherSubConditionEnum.RAGGED, w.sub_condition)

    def test_wrong(self):
        self.assertRaises(ValueError, weather.determine_weather_condition, 999)

    def test_weather(self):
        w = weather.determine_weather_condition(781)
        self.assertEqual((WeatherConditionEnum.ATMOSPHERE, WeatherSubConditionEnum.TORNADO), w.weather_condition)


if __name__ == '__main__':
    unittest.main()
