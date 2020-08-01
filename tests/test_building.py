import json
import unittest

from building import building
from building.blind import Blind
from building.wall import Wall
from shelly.shelly import Shelly


class BuildingTest(unittest.TestCase):
    def test_update(self):
        shelly = Shelly('WS46FD')
        blind = Blind('test', 0, 0, shelly, [])
        wall = Wall('egal', 0, 0)
        wall.blinds = [blind]
        result = building.update_configured_devices([wall], [('testip', get_json())])
        self.assertEqual(1, len(result))
        self.assertEqual(1, len(result[0].blinds))
        self.assertEqual('testip', result[0].blinds[0].device.url)


if __name__ == '__main__':
    unittest.main()


def get_json():
    with open('mock/status.json', 'r') as stream:
        return json.loads(stream.read())
