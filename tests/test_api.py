import json
import unittest

from dateutil import tz, parser

from meteomatics.meteomatics_api import MeteomaticsAPI


class ParseJsonResponse(unittest.TestCase):
    def test_sundata_fill(self):
        api = MeteomaticsAPI()
        sundata = api.process_sundata(get_json(),
                                      parser.parse('2020-07-27T03:59:00Z').astimezone(tz.tzlocal()),
                                      parser.parse('2020-07-27T19:08:00Z').astimezone(tz.tzlocal()))
        self.assertEqual(910, len(sundata.get_positions()))


if __name__ == '__main__':
    unittest.main()


def get_json():
    with open('mock/sundata.json', 'r') as stream:
        return json.loads(stream.read())