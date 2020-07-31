import json
import unittest

from blinds.blind import Blind
from shelly import shelly_finder
from shelly.shelly import Shelly
from blinds.wall import Wall


class ShellyFinder(unittest.TestCase):
    def test_update(self):
        shelly = Shelly('test', 'WS46FD')
        blind = Blind(0, 0, shelly, [])
        wall = Wall('egal', 0, 0)
        wall.blinds = [blind]
        result = shelly_finder.update_configured_shellys([wall], [('testip', get_json())])
        self.assertEqual(1, len(result))
        self.assertEqual(1, len(result[0].blinds))
        self.assertEqual('testip', result[0].blinds[0].shelly.url)


if __name__ == '__main__':
    unittest.main()


def get_json():
    with open('mock/status.json', 'r') as stream:
        return json.loads(stream.read())
