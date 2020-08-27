#!/usr/bin/env python3
import unittest

from yamale import YamaleTestCase


class SettingsTest(YamaleTestCase):
    schema = 'blind_automation/schema.yaml'
    yaml = 'data/settings.yaml.template'

    def test_settings_valid(self):
        self.assertTrue(self.validate())


if __name__ == '__main__':
    unittest.main()
