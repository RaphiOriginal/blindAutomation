#!/usr/bin/env python3
import os
import unittest

from yamale import YamaleTestCase


class SettingsTest(YamaleTestCase):
    def __init__(self):
        print(os.getcwd())
        self.schema = 'blind_automation/schema.yaml'
        self.yaml = 'data/settings.yaml.template'

    def test_settings_valid(self):
        self.assertTrue(self.validate())


if __name__ == '__main__':
    unittest.main()
