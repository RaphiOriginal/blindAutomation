import yaml
import requests
from dateutil import parser, tz

from meteomatics.field import Field
from meteomatics.interval import Interval
from meteomatics.meteomatics_url_builder import MeteomaticsURLBuilder
from settings.settings import Settings


class MeteomaticsAPI:

    def __init__(self):
        self.settingsFile = 'meteomatics/meteomatics.yaml'
        self.url = 'http://api.meteomatics.com'

        self.settings = None

    def get_settings(self):
        if self.settings is None:
            self.settings = Settings(self.settingsFile)
        return self.settings

    def get_auth(self):
        self.settings = self.get_settings()
        return self.settings.get_auth()

    def get_coordinates(self):
        self.settings = self.get_settings()
        return self.settings.get_coordinates()

    def get_sunrise_and_sunset(self):
        try:
            auth = self.get_auth()
            user = auth.user
            password = auth.password

            builder = MeteomaticsURLBuilder(self.url)
            url = builder.add_field(Field.SUNRISE).add_field(Field.SUNSET).set_location(self.get_coordinates()).build()

            r = requests.get(url, auth=(user, password))

            if r.status_code != 200:
                print('Request failed, Status Code: ' + str(r.status_code))
                print(r.text)

            values = r.json()

            sunrise = values.get('data')[0].get('coordinates')[0].get('dates')[0].get('value')
            sunset = values.get('data')[1].get('coordinates')[0].get('dates')[0].get('value')

            return (self.to_date(sunrise), self.to_date(sunset))
        except yaml.YAMLError as exp:
            print(exp)

    @staticmethod
    def to_date(isodate):
        date = parser.parse(isodate)
        return date.astimezone(tz.tzlocal())

    def get_azimuth_time(self, sunrise, sunset, azimuth):
        auth = self.get_auth()
        user = auth.user
        password = auth.password

        builder = MeteomaticsURLBuilder(self.url)
        url = builder.set_time_range(sunrise, sunset).add_field(Field.AZIMUTH) \
            .set_interval(Interval.MINUTELY).set_location(self.get_coordinates()).build()

        r = requests.get(url, auth=(user, password))

        if r.status_code != 200:
            print('Request failed, Status Code: ' + str(r.status_code))
            print(r.text)

        values = r.json().get('data')[0].get('coordinates')[0].get('dates')

        best = -1000.0
        date = ''
        for entry in values:
            if abs(azimuth - best) > abs(azimuth - entry.get('value')):
                best = entry.get('value')
                date = entry.get('date')

        return self.to_date(date)
