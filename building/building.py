import logging

from building.blind import Blind
from building.wall import Wall
from device import device_matcher, device_finder
from settings import settings

logger = logging.getLogger(__name__)


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


def prepare_house():
    walls = prepare_walls()
    device_finder.find_devices(walls)
    return walls
