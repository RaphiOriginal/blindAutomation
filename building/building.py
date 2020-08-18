import logging
import threading

from building.blind import Blind
from building.wall import Wall
from device import device_matcher, device_manager
from device.device import Device
from settings import settings

logger = logging.getLogger(__name__)


class Building:
    def __init__(self, walls):
        self.__walls: [Wall] = walls

    @property
    def walls(self) -> [Wall]:
        return self.__walls

    @property
    def devices(self) -> [Device]:
        return [device for wall in self.walls for device in wall.devices]


def prepare_walls() -> [Wall]:
    walls: [Wall] = []
    data = settings.root
    for item in data.get('walls'):
        wall = item.get('wall')
        w = Wall(wall.get('name'), wall.get('in'), wall.get('out'))
        triggers: [] = []
        if 'blinds' in wall:
            for blind_item in wall.get('blinds'):
                blind = blind_item.get('blind')
                in_sun = w.in_sun
                out_sun = w.out_sun
                controller = device_matcher.create(blind.get('device-id'), blind.get('device-typ'))
                if 'triggers' in blind.keys():
                    triggers = blind.get('triggers')
                if 'in' in blind.keys():
                    in_sun = blind.get('in')
                if 'out' in blind.keys():
                    out_sun = blind.get('out')
                w.add_blind(Blind(blind.get('name'), in_sun, out_sun, controller, triggers))
            walls.append(w)

    return walls


def prepare() -> Building:
    walls = prepare_walls()
    home = prepare.Building(walls)
    manager = threading.Thread(target=device_manager.find_devices, args=(home.devices,), daemon=True)
    manager.start()
    return home


prepare.Building = Building
del Building
