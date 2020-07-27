#!/usr/bin/env python3
from datetime import datetime


class Elevation:
    def __init__(self, time: datetime, degree: float):
        self.time: datetime = time
        self.degree: float = degree

    def __repr__(self):
        return 'Elevation: { time: %s, degree: %s}' % (self.time, self.degree)
