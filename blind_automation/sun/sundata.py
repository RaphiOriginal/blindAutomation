#!/usr/bin/env python3
from datetime import datetime

from blind_automation.sun.azimuth import Azimuth
from blind_automation.sun.elevation import Elevation
from blind_automation.sun.position import Position


class Sundata:
    def __init__(self, sunrise: datetime, sunset: datetime, positions: [Position]):
        self.__sunrise: datetime = sunrise
        self.__sunset: datetime = sunset
        self.__positions: [Position] = positions
        self.__positions.sort(key=lambda p: p.time)

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
        rising = None
        setting = None
        previous = None
        for pos in self.__positions:
            if rising is None:
                rising = pos.elevation()
                previous = rising
                continue
            if setting is None and pos.elevation().degree <= previous.degree:
                setting = previous
            if setting is None:
                rising = self.__check_distance(degree, pos, rising)
            else:
                setting = self.__check_distance(degree, pos, setting)
            previous = pos.elevation()

        return rising, setting

    @staticmethod
    def __check_distance(degree, pos, search) -> Elevation:
        if abs(degree - search.degree) >= abs(degree - pos.elevation().degree):
            return pos.elevation()
        return search

    def get_positions(self):
        return self.__positions

    def get_sunrise(self):
        return self.__sunrise

    def get_sunset(self):
        return self.__sunset

    def __repr__(self):
        return 'Sundata: { sunrise: %s, sunset: %s, positions: %s }' % (self.__sunrise, self.__sunset, self.__positions)
