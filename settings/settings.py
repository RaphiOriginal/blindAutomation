#!/usr/bin/env python3
import logging
from typing import Optional

import yaml
from yamale import yamale

import settings
from settings.coordinates import Coordinates

logger = logging.getLogger(__name__)

root: dict = {}
timezone: str = 'Europe/Zurich'
coordinates: Optional[Coordinates] = None


def convert_coordinates(coords: dict) -> Coordinates:
    if 'alt' in coords.keys():
        return Coordinates(coords.get('lat'), coords.get('long'), coords.get('alt'))
    return Coordinates(coords.get('lat'), coords.get('long'))


def load_settings(settings_file: str = 'settings.yaml'):
    schema = yamale.make_schema('schema.yaml')
    data = yamale.make_data(settings_file)
    yamale.validate(schema, data)
    with open(settings_file, 'r') as stream:
        data = yaml.safe_load(stream)
        settings.settings.root = data
        settings.settings.timezone = data.get('timezone')
        logger.debug('Setting timezone: {}'.format(settings.settings.timezone))
        settings.settings.coordinates = convert_coordinates(data.get('coordinates'))
        logger.debug('Setting coordinates: {}'.format(settings.settings.coordinates))
