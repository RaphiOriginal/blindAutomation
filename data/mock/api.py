#!/usr/bin/env python3
from datetime import datetime, timedelta

from blind_automation.util import dateutil
from blind_automation.api.api import ObservableSunAPI
from blind_automation.sun.azimuth import Azimuth
from blind_automation.sun.elevation import Elevation
from blind_automation.sun.position import Position
from blind_automation.sun.sundata import Sundata


class SunAPIMock(ObservableSunAPI):
    def fetch_sundata(self, date):
        self.sundata = get_sundata_mock()
        return self.sundata


def get_sundata_mock(date: datetime = datetime.now(dateutil.zone), time_delta: int = 10):
    delta = timedelta(seconds=time_delta)
    multiplier = 1
    positions: [Position] = []
    sunrise = date + delta
    for dec in range(50, 310):
        stamp = date + delta * multiplier
        azi = Azimuth(stamp, dec)
        ele = Elevation(stamp, dec / 50)
        if dec > 180:
            ele = Elevation(stamp, (310 - dec) / 50)
        positions.append(Position(stamp, azi, ele))
        multiplier += 1
    sunset = date + delta * 60
    data = Sundata(sunrise, sunset, positions)
    return data
