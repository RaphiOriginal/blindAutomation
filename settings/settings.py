import yaml

from settings.auth import Auth
from settings.coordinates import Coordinates


class Settings:

    __auth = None
    __coordinates = None

    def __init__(self, settingsFile):
        with open(settingsFile, 'r') as stream:
            self.__root = yaml.safe_load(stream)

    def getAuth(self):
        if self.__auth == None:
            auth = self.__root.get('auth')
            self.__auth = Auth(auth.get('username'), auth.get('password'))

        return self.__auth

    def getCoordinates(self):
        if self.__coordinates == None:
            coordinates = self.__root.get('coordinates')
            self.__coordinates = Coordinates(coordinates.get('lat'), coordinates.get('long'))

        return self.__coordinates
