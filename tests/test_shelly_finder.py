import json
import unittest

from shelly import shelly_finder
from shelly.shelly import Shelly
from shelly.wall import Wall


class ShellyFinder(unittest.TestCase):
    def test_update(self):
        shellys = [Shelly('test', 'WS46FD', Wall('test', 0, 0), [])]
        result = shelly_finder.update_configured_shellys(shellys, [('testip', get_json())])
        self.assertEqual(1, len(result))
        self.assertEqual('testip', result[0].url)


if __name__ == '__main__':
    unittest.main()


def get_json():
    with open('mock/status.json', 'r') as stream:
        return json.loads(stream.read())
