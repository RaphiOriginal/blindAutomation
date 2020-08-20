#!/usr/bin/env python3
import yaml
from yamale import yamale

import settings
from settings.coordinates import Coordinates

root = None
timezone: str = 'Europe/Zurich'
coordinates = None


def convert_coordinates(coordinates) -> Coordinates:
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
        settings.settings.coordinates = convert_coordinates(root.get('coordinates'))
