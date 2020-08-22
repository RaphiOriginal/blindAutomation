import unittest
from datetime import datetime

from dateutil.relativedelta import relativedelta, MO, TU, WE, TH, FR, SA, SU

from util import date


class DateTestCase(unittest.TestCase):
    def test_weekday_int(self):
        self.assertEqual('MO', date.weekday(0))
        self.assertEqual('TU', date.weekday(1))
        self.assertEqual('WE', date.weekday(2))
        self.assertEqual('TH', date.weekday(3))
        self.assertEqual('FR', date.weekday(4))
        self.assertEqual('SA', date.weekday(5))
        self.assertEqual('SU', date.weekday(6))

    def test_weekday_datetime(self):
        today = datetime.now()
        monday = relativedelta(weekday=MO)
        self.assertEqual('MO', date.weekday(today + monday))
        tuesday = relativedelta(weekday=TU)
        self.assertEqual('TU', date.weekday(today + tuesday))
        wednesday = relativedelta(weekday=WE)
        self.assertEqual('WE', date.weekday(today + wednesday))
        thursday = relativedelta(weekday=TH)
        self.assertEqual('TH', date.weekday(today + thursday))
        friday = relativedelta(weekday=FR)
        self.assertEqual('FR', date.weekday(today + friday))
        saturday = relativedelta(weekday=SA)
        self.assertEqual('SA', date.weekday(today + saturday))
        sunday = relativedelta(weekday=SU)
        self.assertEqual('SU', date.weekday(today + sunday))

    def test_convert_range(self):
        to_test = 'MO-SU'
        result = date.convert_range(to_test)
        self.assertEqual(7, len(result))
        self.assertEqual(['MO', 'TU', 'WE', 'TH', 'FR', 'SA', 'SU'], result)

    def test_convert_range_overlapping(self):
        to_test = 'TH-WE'
        result = date.convert_range(to_test)
        self.assertEqual(7, len(result))
        self.assertEqual(['TH', 'FR', 'SA', 'SU', 'MO', 'TU', 'WE'], result)

    def test_convert_range_short(self):
        to_test = 'TU-TH'
        result = date.convert_range(to_test)
        self.assertEqual(3, len(result))
        self.assertEqual(['TU', 'WE', 'TH'], result)

    def test_convert_range_empty(self):
        to_test = 'MO'
        result = date.convert_range(to_test)
        self.assertEqual(0, len(result))

    def test_is_workingday_str(self):
        for day in ['MO', 'TU', 'WE', 'TH', 'FR']:
            self.assertTrue(date.is_workingday(day), '{} should be in list'.format(day))
        for day in ['SA', 'SO']:
            self.assertFalse(date.is_workingday(day), '{} should be in list'.format(day))

    def test_is_workingday_int(self):
        for day in [0, 1, 2, 3, 4]:
            self.assertTrue(date.is_workingday(day), '{} should be in list'.format(day))
        for day in [5, 6]:
            self.assertFalse(date.is_workingday(day), '{} should be in list'.format(day))

    def test_is_workingday_datetime(self):
        today = datetime.now()
        monday = relativedelta(weekday=MO)
        self.assertTrue(date.is_workingday(today + monday))
        tuesday = relativedelta(weekday=TU)
        self.assertTrue(date.is_workingday(today + tuesday))
        wednesday = relativedelta(weekday=WE)
        self.assertTrue(date.is_workingday(today + wednesday))
        thursday = relativedelta(weekday=TH)
        self.assertTrue(date.is_workingday(today + thursday))
        friday = relativedelta(weekday=FR)
        self.assertTrue(date.is_workingday(today + friday))
        saturday = relativedelta(weekday=SA)
        self.assertFalse(date.is_workingday(today + saturday))
        sunday = relativedelta(weekday=SU)
        self.assertFalse(date.is_workingday(today + sunday))

    def test_is_weekend_str(self):
        for day in ['MO', 'TU', 'WE', 'TH', 'FR']:
            self.assertFalse(date.is_weekend(day), '{} should be in list'.format(day))
        for day in ['SA', 'SU']:
            self.assertTrue(date.is_weekend(day), '{} should be in list'.format(day))

    def test_is_weekend_int(self):
        for day in [0, 1, 2, 3, 4]:
            self.assertFalse(date.is_weekend(day), '{} should be in list'.format(day))
        for day in [5, 6]:
            self.assertTrue(date.is_weekend(day), '{} should be in list'.format(day))

    def test_is_weekend_datetime(self):
        today = datetime.now()
        monday = relativedelta(weekday=MO)
        self.assertFalse(date.is_weekend(today + monday))
        tuesday = relativedelta(weekday=TU)
        self.assertFalse(date.is_weekend(today + tuesday))
        wednesday = relativedelta(weekday=WE)
        self.assertFalse(date.is_weekend(today + wednesday))
        thursday = relativedelta(weekday=TH)
        self.assertFalse(date.is_weekend(today + thursday))
        friday = relativedelta(weekday=FR)
        self.assertFalse(date.is_weekend(today + friday))
        saturday = relativedelta(weekday=SA)
        self.assertTrue(date.is_weekend(today + saturday))
        sunday = relativedelta(weekday=SU)
        self.assertTrue(date.is_weekend(today + sunday))

    def test_parsing_days(self):
        to_test = ['TU', 'SA']
        result = date.parse_config(to_test)
        self.assertEqual(2, len(result))
        for day in to_test:
            self.assertTrue(day in result, '{} should be in list'.format(day))

    def test_parsing_range(self):
        to_test = ['MO-WE', 'FR-SA']
        result = date.parse_config(to_test)
        self.assertEqual(5, len(result))
        for day in ['MO', 'TU', 'WE', 'FR', 'SA']:
            self.assertTrue(day in result, '{} should be in list'.format(day))

    def test_parsing_workingday(self):
        to_test = ['WORKINGDAY']
        result = date.parse_config(to_test)
        self.assertEqual(5, len(result))
        for day in ['MO', 'TU', 'WE', 'TH', 'FR']:
            self.assertTrue(day in result, '{} should be in list'.format(day))

    def test_parsing_weekend(self):
        to_test = ['WEEKEND']
        result = date.parse_config(to_test)
        self.assertEqual(2, len(result))
        for day in ['SA', 'SU']:
            self.assertTrue(day in result, '{} should be in list'.format(day))

    def test_parsing_mix(self):
        to_test = ['WEEKEND', 'WE-TH', 'MO']
        result = date.parse_config(to_test)
        self.assertEqual(5, len(result))
        for day in ['MO', 'WE', 'TH', 'SA', 'SU']:
            self.assertTrue(day in result, '{} should be in list'.format(day))

    def test_applies_str(self):
        on = ['MO', 'FR']
        self.assertTrue(date.applies('MO', on))
        self.assertTrue(date.applies('FR', on))
        self.assertFalse(date.applies('WE', on))

    def test_applies_int(self):
        on = ['MO', 'FR']
        self.assertTrue(date.applies(0, on))
        self.assertTrue(date.applies(4, on))
        self.assertFalse(date.applies(2, on))

    def test_applies_datetime(self):
        on = ['MO', 'FR']
        today = datetime.now()
        monday = relativedelta(weekday=MO)
        self.assertTrue(date.applies(today + monday, on))
        friday = relativedelta(weekday=FR)
        self.assertTrue(date.applies(today + friday, on))
        wednesday = relativedelta(weekday=WE)
        self.assertFalse(date.applies(today + wednesday, on))

    def test_applies_gibberisch(self):
        on = ['MO', 'FR']
        self.assertFalse(date.applies(7, on))
        self.assertFalse(date.applies('SO', on))


if __name__ == '__main__':
    unittest.main()
