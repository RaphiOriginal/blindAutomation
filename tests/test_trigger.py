import unittest
from datetime import datetime

from dateutil import parser

import global_date
from building.blind import Blind
from jobs import trigger
from jobs.task import Task
from jobs.trigger import SunriseTrigger, SunsetTrigger, SunInTrigger, SunOutTrigger, TimeTrigger, AzimuthTrigger, \
    ElevationTrigger, PositionTrigger
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
        global_date.date.next()
        triggers = [{'TIME': {'task': 'CLOSE', 'time': '16:00:00'}}]
        result = trigger.extract_triggers(blind(triggers), sundata())
        self.assertEqual(1, len(result))
        self.assertEqual(Task.CLOSE, result[0].task())
        for item in result:
            self.assertEqual(TimeTrigger.type(), item.type())
            now = datetime.now(global_date.zone)
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

    def test_offset_minus(self):
        triggers = [{'SUNOUT': {'offset': -8}}]
        result = trigger.extract_triggers(blind(triggers), sundata())
        self.assertEqual(1, len(result))
        self.assertEqual(SunOutTrigger.type(), result[0].type())
        self.assertEqual('2020-07-27T13:00:00+02:00', result[0].time().isoformat())

    def test_azimuth(self):
        triggers = [{'AZIMUTH': {'azimuth': 123}}]
        result = trigger.extract_triggers(blind(triggers), sundata())
        self.assertEqual(1, len(result))
        self.assertEqual(AzimuthTrigger.type(), result[0].type())
        self.assertEqual('2020-07-27T17:08:00+02:00', result[0].time().isoformat())

    def test_elevation_rise(self):
        triggers = [{'ELEVATION': {'elevation': 19, 'direction': 'RISE'}}]
        result = trigger.extract_triggers(blind(triggers), sundata())
        self.assertEqual(1, len(result))
        self.assertEqual(ElevationTrigger.type(), result[0].type())
        self.assertEqual('2020-07-27T13:08:00+02:00', result[0].time().isoformat())

    def test_elevation_set(self):
        triggers = [{'ELEVATION': {'elevation': 19, 'direction': 'SET'}}]
        result = trigger.extract_triggers(blind(triggers), sundata())
        self.assertEqual(1, len(result))
        self.assertEqual(ElevationTrigger.type(), result[0].type())
        self.assertEqual('2020-07-27T21:08:00+02:00', result[0].time().isoformat())

    def test_position(self):
        triggers = [{'POSITION': {'azimuth': 123, 'elevation': 19, 'direction': 'RISE'}}]
        result = trigger.extract_triggers(blind(triggers), sundata())
        self.assertEqual(1, len(result))
        self.assertEqual(PositionTrigger.type(), result[0].type())
        self.assertEqual('2020-07-27T17:08:00+02:00', result[0].time().isoformat())


def blind(triggers: []) -> Blind:
    return Blind('test', 10, 20, None, triggers)


def sundata() -> Sundata:
    sunrise = parser.parse('2020-07-27T03:59:00Z').astimezone(global_date.zone)
    sunset = parser.parse('2020-07-27T19:08:00Z').astimezone(global_date.zone)
    date = parser.parse('2020-07-27T11:08:00Z').astimezone(global_date.zone)
    azimuth = Azimuth(date, 15)
    elevation = Elevation(date, 15)
    position = Position(date, azimuth, elevation)
    date2 = parser.parse('2020-07-27T15:08:00Z').astimezone(global_date.zone)
    azimuth2 = Azimuth(date2, 69)
    elevation2 = Elevation(date2, 23.1)
    position2 = Position(date2, azimuth2, elevation2)
    date3 = parser.parse('2020-07-27T19:08:00Z').astimezone(global_date.zone)
    azimuth3 = Azimuth(date3, 189)
    elevation3 = Elevation(date3, 15)
    position3 = Position(date3, azimuth3, elevation3)
    return Sundata(sunrise, sunset, [position, position2, position3])


if __name__ == '__main__':
    unittest.main()
