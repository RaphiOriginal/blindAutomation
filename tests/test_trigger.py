import unittest
from datetime import datetime

from dateutil import parser, tz

from blinds.blind import Blind
from jobs import trigger
from jobs.task import Task
from jobs.trigger import SunriseTrigger, SunsetTrigger, SunInTrigger, SunOutTrigger, TimeTrigger
from sun.azimuth import Azimuth
from sun.elevation import Elevation
from sun.position import Position
from sun.sundata import Sundata


class TriggerTest(unittest.TestCase):
    def test_extract_sunrise(self):
        triggers = ['SUNRISE', {'SUNRISE': {'task': 'TILT'}}]
        result = trigger.extract_triggers(blind(triggers), sundata())
        self.assertEqual(2, len(result))
        self.assertEqual(Task.OPEN, result[0].task())
        self.assertEqual(Task.TILT, result[1].task())
        for item in result:
            self.assertEqual(SunriseTrigger.type(), item.type())
            self.assertEqual('2020-07-27T05:59:00+02:00', item.time().isoformat())

    def test_extract_sunset(self):
        triggers = ['SUNSET', {'SUNSET': {'task': 'TILT'}}]
        result = trigger.extract_triggers(blind(triggers), sundata())
        self.assertEqual(2, len(result))
        self.assertEqual(Task.CLOSE, result[0].task())
        self.assertEqual(Task.TILT, result[1].task())
        for item in result:
            self.assertEqual(SunsetTrigger.type(), item.type())
            self.assertEqual('2020-07-27T21:08:00+02:00', item.time().isoformat())

    def test_extract_sunin(self):
        triggers = ['SUNIN', {'SUNIN': {'task': 'CLOSE'}}]
        result = trigger.extract_triggers(blind(triggers), sundata())
        self.assertEqual(2, len(result))
        self.assertEqual(Task.TILT, result[0].task())
        self.assertEqual(Task.CLOSE, result[1].task())
        for item in result:
            self.assertEqual(SunInTrigger.type(), item.type())
            self.assertEqual('2020-07-27T13:08:00+02:00', item.time().isoformat())

    def test_extract_sunout(self):
        triggers = ['SUNOUT', {'SUNOUT': {'task': 'TILT'}}]
        result = trigger.extract_triggers(blind(triggers), sundata())
        self.assertEqual(2, len(result))
        self.assertEqual(Task.OPEN, result[0].task())
        self.assertEqual(Task.TILT, result[1].task())
        for item in result:
            self.assertEqual(SunOutTrigger.type(), item.type())
            self.assertEqual('2020-07-27T13:08:00+02:00', item.time().isoformat())

    def test_extract_time(self):
        triggers = [{'TIME': {'task': 'CLOSE', 'time': '16:00:00'}}]
        result = trigger.extract_triggers(blind(triggers), sundata())
        self.assertEqual(1, len(result))
        self.assertEqual(Task.CLOSE, result[0].task())
        for item in result:
            self.assertEqual(TimeTrigger.type(), item.type())
            now = datetime.now(tz.tzlocal())
            self.assertEqual(now.date().isoformat() + 'T16:00:00+02:00', item.time().isoformat())

    def test_no_match(self):
        triggers = ['YOLO', {'YOLO': {'task': 'OPEN'}}]
        result = trigger.extract_triggers(blind(triggers), sundata())
        self.assertEqual(0, len(result))

    def test_offset_plus(self):
        triggers = [{'SUNOUT': {'offset': 2}}]
        result = trigger.extract_triggers(blind(triggers), sundata())
        self.assertEqual(1, len(result))
        self.assertEqual(SunOutTrigger.type(), result[0].type())
        self.assertEqual('2020-07-27T13:10:00+02:00', result[0].time().isoformat())

    def test_offset_plus(self):
        triggers = [{'SUNOUT': {'offset': -8}}]
        result = trigger.extract_triggers(blind(triggers), sundata())
        self.assertEqual(1, len(result))
        self.assertEqual(SunOutTrigger.type(), result[0].type())
        self.assertEqual('2020-07-27T13:00:00+02:00', result[0].time().isoformat())


def blind(triggers: []) -> Blind:
    return Blind('test', 10, 20, None, triggers)


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
