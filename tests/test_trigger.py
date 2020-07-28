import unittest

from dateutil import parser, tz

from jobs import trigger
from jobs.task import Task
from jobs.trigger import SunriseTrigger
from shelly.wall import Wall
from sun.azimuth import Azimuth
from sun.elevation import Elevation
from sun.position import Position
from sun.sundata import Sundata


class TriggerTest(unittest.TestCase):
    def test_extract_Sunrise(self):
        triggers = ['SUNRISE', {'SUNRISE': {'task': 'TILT'}}]
        result = trigger.extract_triggers(triggers, wall(), sundata())
        self.assertEqual(2, len(result))
        self.assertEqual(Task.OPEN, result[0].task())
        self.assertEqual(Task.TILT, result[1].task())
        for item in result:
            self.assertEqual(SunriseTrigger.type(), item.type())
            self.assertEqual('2020-07-27T05:59:00+02:00', item.time().isoformat())


def wall() -> Wall:
    return Wall('name', 10, 20)


def sundata() -> Sundata:
    sunrise = parser.parse('2020-07-27T03:59:00Z').astimezone(tz.tzlocal())
    sunset = parser.parse('2020-07-27T19:08:00Z').astimezone(tz.tzlocal())
    date = parser.parse('2020-07-27T11:08:00Z').astimezone(tz.tzlocal())
    azimuth = Azimuth(date, 15)
    elevation = Elevation(date, 5)
    position = Position(date, azimuth, elevation)
    return Sundata(sunrise, sunset, [position])


if __name__ == '__main__':
    unittest.main()
