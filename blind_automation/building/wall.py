#!/usr/bin/env python3
from .blind.blind import Blind
from ..device.device import Device


class Wall:
    def __init__(self, name: str, in_sun: int, out_sun: int):
        self.name: str = name
        self.in_sun: int = in_sun
        self.out_sun: int = out_sun
        self.blinds: [Blind] = []

    def add_blind(self, blind: Blind):
        self.blinds.append(blind)

    @property
    def devices(self) -> [Device]:
        return list(map(lambda blind: blind.device, self.blinds))

    def __repr__(self):
        return 'Wall: { name: %s, in_sun: %s, out_sun: %s , blinds: %s }' % \
               (self.name, self.in_sun, self.out_sun, self.blinds)
