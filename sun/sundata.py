#!/usr/bin/env python3
from datetime import datetime, timedelta

from sun.azimuth import Azimuth
from sun.elevation import Elevation
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

    def find_elevation(self, degree: float) -> (Elevation, Elevation):
        best = None
        second = None
        for pos in self.__positions:
            if best is None:
                best = pos.elevation()
                continue
            if abs(degree - best.degree) >= abs(degree - pos.elevation().degree):
                if second is None or self.__check_distance(best, second):
                    second = best
                best = pos.elevation()

        if best.time > second.time:
            return second, best
        return best, second

    def __check_distance(self, left, right) -> bool:
        to_check: timedelta = left.time - right.time
        seconds = abs(to_check.seconds)
        return seconds > 60

    def get_positions(self):
        return self.__positions

    def get_sunrise(self):
        return self.__sunrise

    def get_sunset(self):
        return self.__sunset

    def __repr__(self):
        return 'Sundata: { sunrise: %s, sunset: %s, positions: %s }' % (self.__sunrise, self.__sunset, self.__positions)