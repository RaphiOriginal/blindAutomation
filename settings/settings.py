import yaml

from settings.auth import Auth
from settings.coordinates import Coordinates


class Settings:
    __auth = None
    __coordinates = None

    def __init__(self, settingsfile):
        with open(settingsfile, 'r') as stream:
            self.__root = yaml.safe_load(stream)

    def get_auth(self):
        if self.__auth is None:
            auth = self.__root.get('auth')
            self.__auth = Auth(auth.get('username'), auth.get('password'))

        return self.__auth

    def get_coordinates(self):
        if self.__coordinates is None:
            coordinates = self.__root.get('coordinates')
            self.__coordinates = Coordinates(coordinates.get('lat'), coordinates.get('long'))

        return self.__coordinates
