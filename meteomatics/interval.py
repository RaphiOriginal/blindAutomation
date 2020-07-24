#!/usr/bin/env python3
from enum import Enum


class Interval(Enum):
    MINUTELY = ':PT1M'
    HOURLY = ':PT1H'
