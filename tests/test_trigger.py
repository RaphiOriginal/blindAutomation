#!/usr/bin/env python3
import unittest
from datetime import datetime

from dateutil import parser

from blind_automation.util import global_date
from blind_automation.building.blind.blind import Blind
from blind_automation.jobs import trigger
from blind_automation.jobs.task import Tilt, Close, Open
from blind_automation.jobs.trigger import SunriseTrigger, SunsetTrigger, SunInTrigger, SunOutTrigger, TimeTrigger, AzimuthTrigger, \
    ElevationTrigger, PositionTrigger
from blind_automation.sun.azimuth import Azimuth
from blind_automation.sun.elevation import Elevation
from blind_automation.sun.position import Position
from blind_automation.sun.sundata import Sundata


class TriggerTest(unittest.TestCase):
    def test_extract_sunrise(self):
        triggers = ['SUNRISE', {'SUNRISE': {'task': 'TILT'}}]
        result = trigger.extract_triggers(blind(triggers), sundata())
        self.assertEqual(2, len(result))
        self.assertEqual(Open.type(), result[0].task().type())
        self.assertEqual(Tilt.type(), result[1].task().type())
        for item in result:
            self.assertEqual(SunriseTrigger.type(), item.type())
            self.assertEqual('2020-07-27T05:59:00+02:00', item.time().isoformat())

    def test_extract_sunset(self):
        triggers = ['SUNSET', {'SUNSET': {'task': 'TILT'}}]
        result = trigger.extract_triggers(blind(triggers), sundata())
        self.assertEqual(2, len(result))
        self.assertEqual(Close.type(), result[0].task().type())
        self.assertEqual(Tilt.type(), result[1].task().type())
        for item in result:
            self.assertEqual(SunsetTrigger.type(), item.type())
            self.assertEqual('2020-07-27T21:08:00+02:00', item.time().isoformat())

    def test_extract_sunin(self):
        triggers = ['SUNIN', {'SUNIN': {'task': 'CLOSE'}}]
        result = trigger.extract_triggers(blind(triggers), sundata())
        self.assertEqual(2, len(result))
        self.assertEqual(Tilt.type(), result[0].task().type())
        self.assertEqual(Close.type(), result[1].task().type())
        for item in result:
            self.assertEqual(SunInTrigger.type(), item.type())
            self.assertEqual('2020-07-27T05:59:00+02:00', item.time().isoformat())

    def test_extract_sunout(self):
        triggers = ['SUNOUT', {'SUNOUT': {'task': 'TILT'}}]
        result = trigger.extract_triggers(blind(triggers), sundata())
        self.assertEqual(2, len(result))
        self.assertEqual(Open.type(), result[0].task().type())
        self.assertEqual(Tilt.type(), result[1].task().type())
        for item in result:
            self.assertEqual(SunOutTrigger.type(), item.type())
            self.assertEqual('2020-07-27T05:59:00+02:00', item.time().isoformat())

    def test_extract_time(self):
        global_date.date.next()
        triggers = [{'TIME': {'task': 'CLOSE', 'time': '16:00:00'}}]
        result = trigger.extract_triggers(blind(triggers), sundata())
        self.assertEqual(1, len(result))
        self.assertEqual(Close.type(), result[0].task().type())
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
        self.assertEqual('2020-07-27T06:01:00+02:00', result[0].time().isoformat())

    def test_offset_minus(self):
        triggers = [{'SUNOUT': {'offset': -8}}]
        result = trigger.extract_triggers(blind(triggers), sundata())
        self.assertEqual(1, len(result))
        self.assertEqual(SunOutTrigger.type(), result[0].type())
        self.assertEqual('2020-07-27T05:51:00+02:00', result[0].time().isoformat())

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
        self.assertEqual('2020-07-27T05:59:00+02:00', result[0].time().isoformat())

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

    def test_order(self):
        triggers = [{'TIME': {'time': '23:59:59'}}, {'TIME': {'time': '00:00:01'}}, 'SUNOUT', 'SUNIN', 'SUNSET',
                    'SUNRISE']
        result = trigger.extract_triggers(blind(triggers), sundata())
        self.assertEqual(6, len(result))
        self.assertEqual(TimeTrigger.type(), result[4].type())
        now = datetime.now(global_date.zone)
        self.assertEqual(now.date().isoformat() + 'T00:00:01+02:00', result[4].time().isoformat())
        self.assertEqual(SunriseTrigger.type(), result[0].type())
        self.assertEqual(SunInTrigger.type(), result[1].type())
        self.assertEqual(SunOutTrigger.type(), result[2].type())
        self.assertEqual(SunsetTrigger.type(), result[3].type())
        self.assertEqual(TimeTrigger.type(), result[5].type())
        self.assertEqual(now.date().isoformat() + 'T23:59:59+02:00', result[5].time().isoformat())

    def test_sort(self):
        data = sundata()
        triggers = [
            SunOutTrigger(data, 15),
            SunInTrigger(data, 15),
            SunsetTrigger(data),
            SunriseTrigger(data)
        ]
        trigger.sort(triggers)
        self.assertEqual(SunriseTrigger.type(), triggers[0].type())
        self.assertEqual(SunInTrigger.type(), triggers[1].type())
        self.assertEqual(SunOutTrigger.type(), triggers[2].type())
        self.assertEqual(SunsetTrigger.type(), triggers[3].type())

    def test_applies(self):
        triggers = [{'SUNRISE': {'at': ['MO']}}]
        result = trigger.extract_triggers(blind(triggers), sundata())
        self.assertEqual(1, len(result))
        self.assertEqual(Open.type(), result[0].task().type())
        for item in result:
            self.assertEqual(SunriseTrigger.type(), item.type())
            self.assertEqual('2020-07-27T05:59:00+02:00', item.time().isoformat())
            self.assertTrue(item.applies())

    def test_applies_not(self):
        triggers = [{'SUNRISE': {'at': ['TU']}}]
        result = trigger.extract_triggers(blind(triggers), sundata())
        self.assertEqual(1, len(result))
        self.assertEqual(Open.type(), result[0].task().type())
        for item in result:
            self.assertEqual(SunriseTrigger.type(), item.type())
            self.assertEqual('2020-07-27T05:59:00+02:00', item.time().isoformat())
            self.assertFalse(item.applies())

    def test_extract_workingdays(self):
        triggers = [{'SUNRISE': {'at': ['WORKINGDAY']}}]
        result = trigger.extract_triggers(blind(triggers), sundata())
        self.assertEqual(1, len(result))
        self.assertEqual(Open.type(), result[0].task().type())
        self.assertEqual(5, len(result[0]._on))
        for day in result[0]._on:
            self.assertTrue(day in ['MO', 'TU', 'WE', 'TH', 'FR'], 'Day {} not in list {}'.format(day, result[0]._on))

def blind(triggers: []) -> Blind:
    return Blind('test', 10, 20, None, triggers, [])


def sundata() -> Sundata:
    sunrise = parser.parse('2020-07-27T03:59:00Z').astimezone(global_date.zone)
    sunset = parser.parse('2020-07-27T19:08:00Z').astimezone(global_date.zone)
    date = parser.parse('2020-07-27T03:59:00Z').astimezone(global_date.zone)
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
