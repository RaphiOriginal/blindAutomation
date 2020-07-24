from datetime import datetime, timedelta

from dateutil import tz

from sun.azimuth import Azimuth
from sun.sundata import Sundata


def get_sundata_mock(time_delta: int = 10):
    now = datetime.now(tz.tzlocal())
    delta = timedelta(seconds=time_delta)
    multiplier = 1
    azimuth: [Azimuth] = []
    sunrise = now
    for dec in range(50, 310):
        azi = Azimuth(now + delta * multiplier, dec)
        azimuth.append(azi)
        multiplier += 1
    sunset = now + delta * 60
    data = Sundata(sunrise, sunset, azimuth)
    print('Created {}'.format(data))
    return data


