#!/usr/bin/env python3
import unittest
from datetime import datetime

from dateutil.relativedelta import relativedelta, MO, TU, WE, TH, FR, SA, SU

from blind_automation.util import dayutil


class DateTestCase(unittest.TestCase):
    def test_weekday_int(self):
        self.assertEqual('MO', dayutil.weekday(0))
        self.assertEqual('TU', dayutil.weekday(1))
        self.assertEqual('WE', dayutil.weekday(2))
        self.assertEqual('TH', dayutil.weekday(3))
        self.assertEqual('FR', dayutil.weekday(4))
        self.assertEqual('SA', dayutil.weekday(5))
        self.assertEqual('SU', dayutil.weekday(6))

    def test_weekday_datetime(self):
        today = datetime.now()
        monday = relativedelta(weekday=MO)
        self.assertEqual('MO', dayutil.weekday(today + monday))
        tuesday = relativedelta(weekday=TU)
        self.assertEqual('TU', dayutil.weekday(today + tuesday))
        wednesday = relativedelta(weekday=WE)
        self.assertEqual('WE', dayutil.weekday(today + wednesday))
        thursday = relativedelta(weekday=TH)
        self.assertEqual('TH', dayutil.weekday(today + thursday))
        friday = relativedelta(weekday=FR)
        self.assertEqual('FR', dayutil.weekday(today + friday))
        saturday = relativedelta(weekday=SA)
        self.assertEqual('SA', dayutil.weekday(today + saturday))
        sunday = relativedelta(weekday=SU)
        self.assertEqual('SU', dayutil.weekday(today + sunday))

    def test_convert_range(self):
        to_test = 'MO-SU'
        result = dayutil.convert_range(to_test)
        self.assertEqual(7, len(result))
        self.assertEqual(['MO', 'TU', 'WE', 'TH', 'FR', 'SA', 'SU'], result)

    def test_convert_range_overlapping(self):
        to_test = 'TH-WE'
        result = dayutil.convert_range(to_test)
        self.assertEqual(7, len(result))
        self.assertEqual(['TH', 'FR', 'SA', 'SU', 'MO', 'TU', 'WE'], result)

    def test_convert_range_short(self):
        to_test = 'TU-TH'
        result = dayutil.convert_range(to_test)
        self.assertEqual(3, len(result))
        self.assertEqual(['TU', 'WE', 'TH'], result)

    def test_convert_range_empty(self):
        to_test = 'MO'
        result = dayutil.convert_range(to_test)
        self.assertEqual(0, len(result))

    def test_is_workingday_str(self):
        for day in ['MO', 'TU', 'WE', 'TH', 'FR']:
            self.assertTrue(dayutil.is_workingday(day), '{} should be in list'.format(day))
        for day in ['SA', 'SO']:
            self.assertFalse(dayutil.is_workingday(day), '{} should be in list'.format(day))

    def test_is_workingday_int(self):
        for day in [0, 1, 2, 3, 4]:
            self.assertTrue(dayutil.is_workingday(day), '{} should be in list'.format(day))
        for day in [5, 6]:
            self.assertFalse(dayutil.is_workingday(day), '{} should be in list'.format(day))

    def test_is_workingday_datetime(self):
        today = datetime.now()
        monday = relativedelta(weekday=MO)
        self.assertTrue(dayutil.is_workingday(today + monday))
        tuesday = relativedelta(weekday=TU)
        self.assertTrue(dayutil.is_workingday(today + tuesday))
        wednesday = relativedelta(weekday=WE)
        self.assertTrue(dayutil.is_workingday(today + wednesday))
        thursday = relativedelta(weekday=TH)
        self.assertTrue(dayutil.is_workingday(today + thursday))
        friday = relativedelta(weekday=FR)
        self.assertTrue(dayutil.is_workingday(today + friday))
        saturday = relativedelta(weekday=SA)
        self.assertFalse(dayutil.is_workingday(today + saturday))
        sunday = relativedelta(weekday=SU)
        self.assertFalse(dayutil.is_workingday(today + sunday))

    def test_is_weekend_str(self):
        for day in ['MO', 'TU', 'WE', 'TH', 'FR']:
            self.assertFalse(dayutil.is_weekend(day), '{} should be in list'.format(day))
        for day in ['SA', 'SU']:
            self.assertTrue(dayutil.is_weekend(day), '{} should be in list'.format(day))

    def test_is_weekend_int(self):
        for day in [0, 1, 2, 3, 4]:
            self.assertFalse(dayutil.is_weekend(day), '{} should be in list'.format(day))
        for day in [5, 6]:
            self.assertTrue(dayutil.is_weekend(day), '{} should be in list'.format(day))

    def test_is_weekend_datetime(self):
        today = datetime.now()
        monday = relativedelta(weekday=MO)
        self.assertFalse(dayutil.is_weekend(today + monday))
        tuesday = relativedelta(weekday=TU)
        self.assertFalse(dayutil.is_weekend(today + tuesday))
        wednesday = relativedelta(weekday=WE)
        self.assertFalse(dayutil.is_weekend(today + wednesday))
        thursday = relativedelta(weekday=TH)
        self.assertFalse(dayutil.is_weekend(today + thursday))
        friday = relativedelta(weekday=FR)
        self.assertFalse(dayutil.is_weekend(today + friday))
        saturday = relativedelta(weekday=SA)
        self.assertTrue(dayutil.is_weekend(today + saturday))
        sunday = relativedelta(weekday=SU)
        self.assertTrue(dayutil.is_weekend(today + sunday))

    def test_parsing_days(self):
        to_test = ['TU', 'SA']
        result = dayutil.parse_config(to_test)
        self.assertEqual(2, len(result))
        for day in to_test:
            self.assertTrue(day in result, '{} should be in list'.format(day))

    def test_parsing_range(self):
        to_test = ['MO-WE', 'FR-SA']
        result = dayutil.parse_config(to_test)
        self.assertEqual(5, len(result))
        for day in ['MO', 'TU', 'WE', 'FR', 'SA']:
            self.assertTrue(day in result, '{} should be in list'.format(day))

    def test_parsing_workingday(self):
        to_test = ['WORKINGDAY']
        result = dayutil.parse_config(to_test)
        self.assertEqual(5, len(result))
        for day in ['MO', 'TU', 'WE', 'TH', 'FR']:
            self.assertTrue(day in result, '{} should be in list'.format(day))

    def test_parsing_weekend(self):
        to_test = ['WEEKEND']
        result = dayutil.parse_config(to_test)
        self.assertEqual(2, len(result))
        for day in ['SA', 'SU']:
            self.assertTrue(day in result, '{} should be in list'.format(day))

    def test_parsing_mix(self):
        to_test = ['WEEKEND', 'WE-TH', 'MO']
        result = dayutil.parse_config(to_test)
        self.assertEqual(5, len(result))
        for day in ['MO', 'WE', 'TH', 'SA', 'SU']:
            self.assertTrue(day in result, '{} should be in list'.format(day))

    def test_parsing_overlapping(self):
        to_test = ['WEEKEND', 'WORKINGDAY', 'MO', 'TU', 'WE', 'TH', 'FR', 'SA', 'SU', 'MO-SU']
        result = dayutil.parse_config(to_test)
        self.assertEqual(7, len(result))
        for day in ['MO', 'TU', 'WE', 'TH', 'FR', 'SA', 'SU']:
            self.assertTrue(day in result, '{} should be in list'.format(day))

    def test_parsing_mix_with_wrongs(self):
        to_test = ['SO', 'MO']
        result = dayutil.parse_config(to_test)
        self.assertEqual(1, len(result))
        self.assertEqual('MO', result[0])
        to_test = ['MO', 'SO']
        result = dayutil.parse_config(to_test)
        self.assertEqual(1, len(result))
        self.assertEqual('MO', result[0])

    def test_applies_str(self):
        on = ['MO', 'FR']
        self.assertTrue(dayutil.applies('MO', on))
        self.assertTrue(dayutil.applies('FR', on))
        self.assertFalse(dayutil.applies('WE', on))

    def test_applies_int(self):
        on = ['MO', 'FR']
        self.assertTrue(dayutil.applies(0, on))
        self.assertTrue(dayutil.applies(4, on))
        self.assertFalse(dayutil.applies(2, on))

    def test_applies_datetime(self):
        on = ['MO', 'FR']
        today = datetime.now()
        monday = relativedelta(weekday=MO)
        self.assertTrue(dayutil.applies(today + monday, on))
        friday = relativedelta(weekday=FR)
        self.assertTrue(dayutil.applies(today + friday, on))
        wednesday = relativedelta(weekday=WE)
        self.assertFalse(dayutil.applies(today + wednesday, on))

    def test_applies_gibberisch(self):
        on = ['MO', 'FR']
        self.assertFalse(dayutil.applies(7, on))
        self.assertFalse(dayutil.applies('SO', on))


if __name__ == '__main__':
    unittest.main()
