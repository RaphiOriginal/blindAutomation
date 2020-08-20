import unittest

from weather import weather
from weather.weather import Clear, Clouds, Atmosphere, Snow, Rain, Drizzle, Storm


class WeatherTestCase(unittest.TestCase):
    def test_clear(self):
        w = weather.determine_weather(800)
        self.assertEqual(Clear.type(), w.type())

    def test_clouds(self):
        for code in [801, 802, 803, 804]:
            w = weather.determine_weather(code)
            self.assertEqual(Clouds.type(), w.type())

    def test_atmosphere(self):
        for code in [701, 711, 721, 731, 741, 751, 761, 762, 771, 781]:
            w = weather.determine_weather(code)
            self.assertEqual(Atmosphere.type(), w.type())

    def test_snow(self):
        for code in [600, 601, 602, 611, 612, 613, 615, 616, 620, 621, 622]:
            w = weather.determine_weather(code)
            self.assertEqual(Snow.type(), w.type())

    def test_rain(self):
        for code in [500, 501, 502, 503, 504, 511, 520, 521, 522, 531]:
            w = weather.determine_weather(code)
            self.assertEqual(Rain.type(), w.type())

    def test_drizzle(self):
        for code in [300, 301, 302, 310, 311, 312, 313, 314, 321]:
            w = weather.determine_weather(code)
            self.assertEqual(Drizzle.type(), w.type())

    def test_storm(self):
        for code in [200, 201, 202, 210, 211, 212, 221, 230, 231, 232]:
            w = weather.determine_weather(code)
            self.assertEqual(Storm.type(), w.type())


if __name__ == '__main__':
    unittest.main()
