#!/usr/bin/env python3
from datetime import datetime

from blind_automation.sun.azimuth import Azimuth
from blind_automation.sun.elevation import Elevation


class Position:
    def __init__(self, time: datetime, azimuth: Azimuth, elevation: Elevation):
        self.time: datetime = time
        self.__azimuth: Azimuth = azimuth
        self.__elevation: Elevation = elevation

    def azimuth(self) -> Azimuth:
        return self.__azimuth

    def elevation(self) -> Elevation:
        return self.__elevation

    def __repr__(self):
        return 'Position: { time: %s, azimuth: %s, elevation: %s }' % (self.time, self.__azimuth, self.__elevation)
