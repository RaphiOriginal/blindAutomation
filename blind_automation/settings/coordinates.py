#!/usr/bin/env python3
class Coordinates:
    def __init__(self, lat: float, long: float, alt: int = 0):
        self.lat: float = lat
        self.long: float = long
        self.alt: int = alt

    def __repr__(self):
        return 'Coordinates: {latitude: %s, longitude: %s, altitude: %s}' % (self.lat, self.long, self.alt)