#!/usr/bin/env python3
import yaml
from yamale import yamale

import settings
from settings.auth import Auth
from settings.coordinates import Coordinates

root = None


class APISettings:
    __auth = None
    __coordinates = None

    def __init__(self):
        if settings.settings.root is not None:
            self.__root = settings.settings.root.get('meteomatics')

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


class NetworkSettings:
    def __init__(self):
        if settings.settings.root is not None:
            self.mask = settings.settings.root.get('networkmask')


def load_settings():
    schema = yamale.make_schema('schema.yaml')
    data = yamale.make_data('settings.yaml')
    yamale.validate(schema, data)
    with open('settings.yaml', 'r') as stream:
        settings.settings.root = yaml.safe_load(stream)
