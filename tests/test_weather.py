import unittest

from weather.enum import WeatherSubConditionEnum
from weather.weather import WeatherConditionEnum, Condition


class WeatherTestCase(unittest.TestCase):
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


if __name__ == '__main__':
    unittest.main()
