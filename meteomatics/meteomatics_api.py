#!/usr/bin/env python3
import logging
from collections import defaultdict
from datetime import datetime

import requests
import yaml
from dateutil import parser

import global_date
from api.api import ObservableSunAPI
from meteomatics.field import Field
from meteomatics.interval import Interval
from meteomatics.meteomatics_url_builder import MeteomaticsURLBuilder
from settings.settings import MeteomaticsSettings
from sun.azimuth import Azimuth
from sun.elevation import Elevation
from sun.position import Position
from sun.sundata import Sundata

logger = logging.getLogger(__name__)


class MeteomaticsAPI(ObservableSunAPI):

    def __init__(self):
        super(MeteomaticsAPI, self).__init__()
        self.url = 'http://api.meteomatics.com'

        self.settings = None

    def fetch_sundata(self, date: datetime):
        """Returns Sundata object containing array of azimuth per minute between sunrise and sunset, sunrise and
        sunset """
        auth = self.__get_auth()
        user = auth.user
        password = auth.password

        (sunrise, sunset) = self.__fetch_sunrise_and_sunset(date, auth)

        builder = MeteomaticsURLBuilder(self.url)
        url = builder.set_time_range(sunrise, sunset).add_field(Field.AZIMUTH).add_field(Field.ELEVATION) \
            .set_interval(Interval.MINUTELY).set_location(self.__get_coordinates()).build()

        r = requests.get(url, auth=(user, password))

        if r.status_code != 200:
            logger.error('Request failed, Status Code: ' + str(r.status_code))
            logger.info(r.text)

        return self.process_sundata(r.json(), sunrise, sunset)

    def process_sundata(self, json, sunrise, sunset):
        directions = json.get('data')
        azimuth = defaultdict(Azimuth)
        elevation = defaultdict(Elevation)
        dates = set()
        for item in directions:
            if Field.AZIMUTH.value == item.get('parameter'):
                values = item.get('coordinates')[0].get('dates')

                for entry in values:
                    date = entry.get('date')
                    azimuth[date] = self.__convert_to_azimuth(date, entry.get('value'))
                    dates.add(date)

            if Field.ELEVATION.value == item.get('parameter'):
                values = item.get('coordinates')[0].get('dates')

                for entry in values:
                    date = entry.get('date')
                    elevation[date] = self.__convert_to_elevation(date, entry.get('value'))
                    dates.add(date)
        sun_positions: [Position] = []
        for date in dates:
            a = azimuth.get(date)
            e = elevation.get(date)
            sun_positions.append(Position(date, a, e))
        self.sundata = Sundata(sunrise, sunset, sun_positions)
        logger.debug('Fetched {}'.format(self.sundata))
        self.notify()
        return self.sundata

    def __fetch_sunrise_and_sunset(self, date: datetime, auth):
        try:
            user = auth.user
            password = auth.password

            builder = MeteomaticsURLBuilder(self.url)

            logger.info('Fetching sunrise and sunset for {}'.format(date))
            url = builder.set_time(date).add_field(Field.SUNRISE).add_field(Field.SUNSET) \
                .set_location(self.__get_coordinates()).build()

            r = requests.get(url, auth=(user, password))

            if r.status_code != 200:
                logger.error('Request failed, Status Code: ' + str(r.status_code))
                logger.info(r.text)

            values = r.json()

            sunrise = values.get('data')[0].get('coordinates')[0].get('dates')[0].get('value')
            sunset = values.get('data')[1].get('coordinates')[0].get('dates')[0].get('value')

            return self.__to_date(sunrise), self.__to_date(sunset)
        except yaml.YAMLError as exp:
            logger.error(exp)

    @staticmethod
    def __to_date(isodate):
        date = parser.parse(isodate)
        return date.astimezone(global_date.zone)

    def __convert_to_azimuth(self, date: str, degree: float):
        return Azimuth(self.__to_date(date), degree)

    def __convert_to_elevation(self, date: str, degree: float):
        return Elevation(self.__to_date(date), degree)

    def __get_settings(self):
        if self.settings is None:
            self.settings = MeteomaticsSettings()
        return self.settings

    def __get_auth(self):
        self.settings = self.__get_settings()
        return self.settings.get_auth()

    def __get_coordinates(self):
        self.settings = self.__get_settings()
        return self.settings.get_coordinates()

    @property
    def __repr__(self):
        return 'MeteomaticsAPI to get sunrise, sunset and sun positions in a time array'
