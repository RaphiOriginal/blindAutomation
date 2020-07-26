#!/usr/bin/env python3
class Wall:
    def __init__(self, name: str, in_sun: int, out_sun: int):
        self.__name: str = name
        self.__in_sun: int = in_sun
        self.__out_sun: int = out_sun

    def in_sun(self):
        return self.__in_sun

    def out_sun(self):
        return self.__out_sun

    def __repr__(self):
        return 'Wall: { name: %s, in_sun: %s, out_sun: %s }' % (self.__name, self.__in_sun, self.__out_sun)
