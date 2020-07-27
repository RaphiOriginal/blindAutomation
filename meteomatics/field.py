#!/usr/bin/env python3
from enum import Enum


class Field(Enum):
    SUNRISE = 'sunrise:sql'
    SUNSET = 'sunset:sql'
    AZIMUTH = 'sun_azimuth:d'
    ELEVATION = 'sun_elevation:d'
