import unittest

from yamale import yamale


class SettingsTest(unittest.TestCase):
    def test_settings_valid(self):
        schema = yamale.make_schema('../schema.yaml')
        data = yamale.make_data('../settings.yaml.template')
        yamale.validate(schema, data)


if __name__ == '__main__':
    unittest.main()
