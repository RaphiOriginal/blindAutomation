#!/usr/bin/env python3
import logging
import threading

from .blind.blind import Blind
from .wall import Wall
from ..device import matcher
from ..device.device import Device
from ..device.manager import DeviceManager
from ..settings import settings

logger = logging.getLogger(__name__)


class Building:
    def __init__(self, walls):
        self.__walls: [Wall] = walls

    @property
    def walls(self) -> [Wall]:
        return self.__walls

    @property
    def blinds(self) -> [Blind]:
        return [blind for wall in self.walls for blind in wall.blinds]

    @property
    def devices(self) -> [Device]:
        return [device for wall in self.walls for device in wall.devices]


def prepare_walls() -> [Wall]:
    walls: [Wall] = []
    data = settings.root
    for item in data.get('walls'):
        wall = item.get('wall')
        w = Wall(wall.get('name'), wall.get('in'), wall.get('out'))
        if 'blinds' in wall:
            for blind_item in wall.get('blinds'):
                triggers: [] = []
                events: [] = []
                blind = blind_item.get('blind')
                in_sun = w.in_sun
                out_sun = w.out_sun
                controller = matcher.create(blind.get('device-id'), blind.get('device-typ'))
                if 'triggers' in blind.keys():
                    triggers = blind.get('triggers')
                if 'events' in blind.keys():
                    events = blind.get('events')
                if 'in' in blind.keys():
                    in_sun = blind.get('in')
                if 'out' in blind.keys():
                    out_sun = blind.get('out')
                b = Blind(blind.get('name'), in_sun, out_sun, controller, triggers, events)
                if 'tilt_time' in blind.keys():
                    b.override_tilt_duration(blind.get('tilt_time'))
                w.add_blind(b)
            walls.append(w)

    return walls


def prepare() -> Building:
    walls = prepare_walls()
    home = prepare.Building(walls)
    manager = threading.Thread(target=DeviceManager(home.devices).run, daemon=True)
    manager.start()
    return home


prepare.Building = Building
del Building
