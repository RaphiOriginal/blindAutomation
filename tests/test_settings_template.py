import unittest

from yamale import YamaleTestCase


class SettingsTest(YamaleTestCase):
    schema = 'schema.yaml'
    yaml = 'settings.yaml.template'

    def test_settings_valid(self):
        self.assertTrue(self.validate())


if __name__ == '__main__':
    unittest.main()
