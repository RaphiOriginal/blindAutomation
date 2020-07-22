import datetime
import math

import yaml
import requests
from dateutil import parser, tz

settingsFile = 'settings.yaml'
url = 'http://api.meteomatics.com/'
fields = 'sunrise:sql,sunset:sql'
field = 'sun_azimuth:d'
json = 'json'
csv = 'csv'

def readSettings():
    with open(settingsFile, 'r') as stream:
        return yaml.safe_load(stream)

def getAuth():
    settings = readSettings()
    return settings.get('auth')

def getCoordinates():
    settings = readSettings()
    return settings.get('coordinates')

def buildLocation():
    coordinates = getCoordinates()
    return '{},{}'.format(coordinates.get('lat'), coordinates.get('long'))


def getSunriseAndSunset():
    try:
        auth = getAuth()
        user = auth.get('username')
        password = auth.get('password')

        time = 'now'
        location = buildLocation()

        r = requests.get(url + time + '/' + fields + '/' + location + '/' + json, auth=(user, password))

        if r.status_code != 200:
            print('Request failed, Status Code: ' + r.status_code)

        values = r.json()
        print(values)

        sunrise = values.get('data')[0].get('coordinates')[0].get('dates')[0].get('value')
        sunset = values.get('data')[1].get('coordinates')[0].get('dates')[0].get('value')

        return (toDate(sunrise), toDate(sunset))
    except yaml.YAMLError as exp:
        print(exp)

def toDate(isoDate):
    date = parser.parse(isoDate)
    return date.astimezone(tz.tzlocal())

def getAzimuthTime(sunrise, sunset, azimuth):
    auth = getAuth()
    user = auth.get('username')
    password = auth.get('password')

    time = '{}--{}:PT1M'.format(sunrise.isoformat(), sunset.isoformat())
    location = buildLocation()

    r = requests.get(url + time + '/' + field + '/' + location + '/' + json, auth=(user, password))

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

    return toDate(date)

(sunrise, sunset) = getSunriseAndSunset()
print(getAzimuthTime(sunrise, sunset, 110.0))
print(getAzimuthTime(sunrise, sunset, 290.0))