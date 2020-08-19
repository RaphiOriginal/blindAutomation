import json
from datetime import datetime, timedelta

from dateutil import parser

import global_date
from api.api import ObservableSunAPI
from meteomatics.meteomatics_api import MeteomaticsAPI
from sun.azimuth import Azimuth
from sun.elevation import Elevation
from sun.position import Position
from sun.sundata import Sundata


class SunAPIMock(ObservableSunAPI):
    def fetch_sundata(self, date):
        return get_sundata_mock(date)


def get_sundata_mock(now, time_delta: int = 30):
    delta = timedelta(seconds=time_delta)
    now = datetime.now(global_date.zone)
    multiplier = 1
    positions: [Position] = []
    sunrise = now + delta
    for dec in range(50, 310):
        stamp = now + delta * multiplier
        azi = Azimuth(stamp, dec)
        ele = Elevation(stamp, dec / 50)
        if dec > 180:
            ele = Elevation(stamp, (310 - dec) / 50)
        positions.append(Position(stamp, azi, ele))
        multiplier += 1
    sunset = now + delta * 60
    data = Sundata(sunrise, sunset, positions)
    return data


class SunAPIResponseMock(ObservableSunAPI):
    def fetch_sundata(self):
        api = MeteomaticsAPI()
        return api.process_sundata(get_json(),
                                   parser.parse('2020-07-27T03:59:00Z').astimezone(global_date.zone),
                                   parser.parse('2020-07-27T19:08:00Z').astimezone(global_date.zone))


def get_json():
    with open('tests/mock/sundata.json', 'r') as stream:
        return json.loads(stream.read())
