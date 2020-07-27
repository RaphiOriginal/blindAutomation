import json
from datetime import datetime, timedelta

from dateutil import tz, parser

from api.api import SunAPI
from meteomatics.meteomatics_api import MeteomaticsAPI
from sun.azimuth import Azimuth
from sun.elevation import Elevation
from sun.position import Position
from sun.sundata import Sundata


class SunAPIMock(SunAPI):
    def fetch_sundata(self):
        return get_sundata_mock()


def get_sundata_mock(time_delta: int = 10):
    now = datetime.now(tz.tzlocal())
    delta = timedelta(seconds=time_delta)
    multiplier = 1
    positions: [Position] = []
    sunrise = now
    for dec in range(50, 310):
        stamp = now + delta * multiplier
        azi = Azimuth(stamp, dec)
        ele = Elevation(stamp, dec / 50)
        positions.append(Position(stamp, azi, ele))
        multiplier += 1
    sunset = now + delta * 60
    data = Sundata(sunrise, sunset, positions)
    print('Created {}'.format(data))
    return data


class SunAPIResponseMock(SunAPI):
    def fetch_sundata(self):
        api = MeteomaticsAPI()
        return api.process_sundata(get_json(),
                                   parser.parse('2020-07-27T03:59:00Z').astimezone(tz.tzlocal()),
                                   parser.parse('2020-07-27T19:08:00Z').astimezone(tz.tzlocal()))


def get_json():
    with open('tests/mock/sundata.json', 'r') as stream:
        return json.loads(stream.read())
