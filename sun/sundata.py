from datetime import datetime

from sun.azimuth import Azimuth


class Sundata:
    def __init__(self, sunrise: datetime, sunset: datetime, azimuths: [Azimuth]):
        self.__sunrise: datetime = sunrise
        self.__sunset: datetime = sunset
        self.__azimuths: [Azimuth] = azimuths

    def find_azimuth(self, degree: float):
        best = None
        for azimuth in self.__azimuths:
            if best is None:
                best = azimuth
                continue
            if abs(degree - best.degree) > abs(degree - azimuth.degree):
                best = azimuth

        return best

    def get_sunrise(self):
        return self.__sunrise

    def get_sunset(self):
        return self.__sunset
