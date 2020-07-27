#!/usr/bin/env python3
import logging
from datetime import datetime, timedelta

import yaml
import requests
from dateutil import parser, tz

from meteomatics.field import Field
from meteomatics.interval import Interval
from meteomatics.meteomatics_url_builder import MeteomaticsURLBuilder
from settings.settings import APISettings
from sun.azimuth import Azimuth
from sun.sundata import Sundata


logger = logging.getLogger(__name__)


class MeteomaticsAPI:

    def __init__(self):
        self.settingsFile = 'settings.yaml'
        self.url = 'http://api.meteomatics.com'

        self.settings = None

    def fetch_sundata(self):
        """Returns Sundata object containing array of azimuth per minute between sunrise and sunset, sunrise and
        sunset """
        auth = self.__get_auth()
        user = auth.user
        password = auth.password

        (sunrise, sunset) = self.__fetch_sunrise_and_sunset(auth)

        builder = MeteomaticsURLBuilder(self.url)
        url = builder.set_time_range(sunrise, sunset).add_field(Field.AZIMUTH) \
            .set_interval(Interval.MINUTELY).set_location(self.__get_coordinates()).build()

        r = requests.get(url, auth=(user, password))

        if r.status_code != 200:
            logger.error('Request failed, Status Code: ' + str(r.status_code))
            logger.info(r.text)

        values = r.json().get('data')[0].get('coordinates')[0].get('dates')

        azimuth = []
        for entry in values:
            azimuth.append(self.__convert_to_azimuth(entry.get('date'), entry.get('value')))

        sundata = Sundata(sunrise, sunset, azimuth)
        logger.info('Fetched {}'.format(sundata))
        return sundata

    def __fetch_sunrise_and_sunset(self, auth):
        try:
            user = auth.user
            password = auth.password

            builder = MeteomaticsURLBuilder(self.url)

            #Hacky solution to avoid old data between 24:00 and 02:00
            now = datetime.now(tz.tzlocal()) + timedelta(hours=2)
            logger.info('Fetching sunrise and sunset for {}'.format(now))
            url = builder.set_time(now).add_field(Field.SUNRISE).add_field(Field.SUNSET)\
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
        return date.astimezone(tz.tzlocal())

    def __convert_to_azimuth(self, date:str, degree: float):
        return Azimuth(self.__to_date(date), degree)

    def __get_settings(self):
        if self.settings is None:
            self.settings = APISettings(self.settingsFile)
        return self.settings

    def __get_auth(self):
        self.settings = self.__get_settings()
        return self.settings.get_auth()

    def __get_coordinates(self):
        self.settings = self.__get_settings()
        return self.settings.get_coordinates()
