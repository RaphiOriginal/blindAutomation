#!/usr/bin/env python3
from datetime import datetime

from sun.azimuth import Azimuth
from sun.position import Position


class Sundata:
    def __init__(self, sunrise: datetime, sunset: datetime, positions: [Position]):
        self.__sunrise: datetime = sunrise
        self.__sunset: datetime = sunset
        self.__positions: [Position] = positions

    def find_azimuth(self, degree: float) -> Azimuth:
        best = None
        for pos in self.__positions:
            if best is None:
                best = pos.azimuth()
                continue
            if abs(degree - best.degree) > abs(degree - pos.azimuth().degree):
                best = pos.azimuth()

        return best

    def get_positions(self):
        return self.__positions

    def get_sunrise(self):
        return self.__sunrise

    def get_sunset(self):
        return self.__sunset

    def __repr__(self):
        return 'Sundata: { sunrise: %s, sunset: %s, positions: %s }' % (self.__sunrise, self.__sunset, self.__positions)