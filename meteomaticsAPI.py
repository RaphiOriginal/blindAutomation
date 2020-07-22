import yaml
import requests
from dateutil import parser, tz

from settings import Settings

class MeteomaticsAPI:

    def __init__(self):
        self.settingsFile = 'meteomatics.yaml'
        self.url = 'http://api.meteomatics.com/'
        self.fields = 'sunrise:sql,sunset:sql'
        self.field = 'sun_azimuth:d'
        self.json = 'json'
        self.csv = 'csv'

        self.settings = None

    def getSettings(self):
        if self.settings == None:
            self.settings = Settings(self.settingsFile)
        return self.settings

    def getAuth(self):
        self.settings = self.getSettings()
        return self.settings.getAuth()

    def getCoordinates(self):
        self.settings = self.getSettings()
        return self.settings.getCoordinates()

    def buildLocation(self):
        coordinates = self.getCoordinates()
        return '{},{}'.format(coordinates.lat, coordinates.long)


    def getSunriseAndSunset(self):
        try:
            auth = self.getAuth()
            user = auth.user
            password = auth.password

            time = 'now'
            location = self.buildLocation()

            r = requests.get(self.url + time + '/' + self.fields + '/' + location + '/' + self.json, auth=(user, password))

            if r.status_code != 200:
                print('Request failed, Status Code: ' + r.status_code)

            values = r.json()
            print(values)

            sunrise = values.get('data')[0].get('coordinates')[0].get('dates')[0].get('value')
            sunset = values.get('data')[1].get('coordinates')[0].get('dates')[0].get('value')

            return (self.toDate(sunrise), self.toDate(sunset))
        except yaml.YAMLError as exp:
            print(exp)

    def toDate(self, isoDate):
        date = parser.parse(isoDate)
        return date.astimezone(tz.tzlocal())

    def getAzimuthTime(self, sunrise, sunset, azimuth):
        auth = self.getAuth()
        user = auth.user
        password = auth.password

        time = '{}--{}:PT1M'.format(sunrise.isoformat(), sunset.isoformat())
        location = self.buildLocation()

        r = requests.get(self.url + time + '/' + self.field + '/' + location + '/' + self.json, auth=(user, password))

        if r.status_code != 200:
            print('Request failed, Status Code: ' + str(r.status_code))

        values = r.json().get('data')[0].get('coordinates')[0].get('dates')

        print(values)

        best = -1000.0
        date = ''
        for entry in values:
            if abs(azimuth - best) > abs(azimuth - entry.get('value')):
                best = entry.get('value')
                date = entry.get('date')

        return self.toDate(date)

api = MeteomaticsAPI()
(sunrise, sunset) = api.getSunriseAndSunset()
print(api.getAzimuthTime(sunrise, sunset, 110.0))
print(api.getAzimuthTime(sunrise, sunset, 290.0))