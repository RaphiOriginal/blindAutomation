import logging
from collections import defaultdict
from datetime import datetime

import pandas
import pvlib

from api.api import SunAPI
from settings.settings import PvLibSettings
from sun.azimuth import Azimuth
from sun.elevation import Elevation
from sun.position import Position
from sun.sundata import Sundata

logger = logging.getLogger(__name__)


class PVLibAPI(SunAPI):
    def __init__(self):
        config = PvLibSettings()
        coordinates = config.get_coordinates()
        self.__location = pvlib.location.Location(coordinates.lat, coordinates.long, tz='Europe/Zurich',
                                                  altitude=coordinates.alt)

    def fetch_sundata(self, date: datetime):
        timestamp = pandas.Timestamp(date.isoformat())
        datetime = pandas.to_datetime(timestamp)
        sunrise, sunset = self.__calculate_sunrise_sunset(datetime)
        times = pandas.date_range(start=sunrise, end=sunset, freq='1min')
        solarpositions = self.__location.get_solarposition(times)
        azimuthpos = solarpositions.azimuth
        elevationpos = solarpositions.elevation

        azimuth = defaultdict(Azimuth)
        elevation = defaultdict(Elevation)
        dates = set()

        for item in azimuthpos.items():
            date = self.__to_date(item[0])
            azimuth[date] = Azimuth(date, item[1])
            dates.add(date)

        for item in elevationpos.items():
            date = self.__to_date(item[0])
            elevation[date] = Elevation(date, item[1])
            dates.add(date)

        sun_positions: [Position] = []
        for date in dates:
            a = azimuth.get(date)
            e = elevation.get(date)
            sun_positions.append(Position(date, a, e))

        sundata = Sundata(self.__to_date(sunrise), self.__to_date(sunset), sun_positions)
        logger.debug('Created {}'.format(sundata))
        return sundata

    def __calculate_sunrise_sunset(self, date):
        result = self.__location.get_sun_rise_set_transit(pandas.DatetimeIndex([date]))
        return result.sunrise[0], result.sunset[0]

    def __to_date(self, date) -> datetime:
        return datetime.fromisoformat(date.isoformat())
