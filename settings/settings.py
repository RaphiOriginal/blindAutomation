#!/usr/bin/env python3
import yaml
from yamale import yamale

import settings
from settings.auth import Auth
from settings.coordinates import Coordinates

root = None
timezone: str = 'Europe/Zurich'


class MeteomaticsSettings:
    __auth = None
    __coordinates = None

    def __init__(self):
        if settings.settings.root is not None:
            self.__root = settings.settings.root.get('meteomatics')

    def get_auth(self):
        if self.__auth is None:
            self.__auth = get_auth(self.__root)

        return self.__auth

    def get_coordinates(self):
        if self.__coordinates is None:
            self.__coordinates = get_coordinates(self.__root)

        return self.__coordinates


class PvLibSettings:
    __coordinates = None

    def __init__(self):
        if settings.settings.root is not None:
            self.__root = settings.settings.root.get('pvlib')

    def get_coordinates(self):
        if self.__coordinates is None:
            self.__coordinates = get_coordinates(self.__root)

        return self.__coordinates


def get_auth(api_root) -> Auth:
    auth = api_root.get('auth')
    return Auth(auth.get('username'), auth.get('password'))


def get_coordinates(api_root) -> Coordinates:
    coordinates = api_root.get('coordinates')
    if 'alt' in coordinates.keys():
        return Coordinates(coordinates.get('lat'), coordinates.get('long'), coordinates.get('alt'))
    return Coordinates(coordinates.get('lat'), coordinates.get('long'))


def load_settings():
    schema = yamale.make_schema('schema.yaml')
    data = yamale.make_data('settings.yaml')
    yamale.validate(schema, data)
    with open('settings.yaml', 'r') as stream:
        settings.settings.root = yaml.safe_load(stream)
        settings.settings.timezone = settings.settings.root.get('timezone')
