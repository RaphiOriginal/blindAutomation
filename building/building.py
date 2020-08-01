import logging

import yaml

from building.blind import Blind
from building.wall import Wall
from shelly.shelly import Shelly


config = 'settings.yaml'

logger = logging.getLogger(__name__)


def prepare_walls() -> [Wall]:
    walls: [Wall] = []
    with open(config, 'r') as stream:
        data = yaml.safe_load(stream)
        for item in data.get('walls'):
            wall = item.get('wall')
            w = Wall(wall.get('name'), wall.get('in'), wall.get('out'))
            triggers: [] = []
            if 'blinds' in wall:
                for blind_item in wall.get('blinds'):
                    blind = blind_item.get('blind')
                    in_sun = w.in_sun
                    out_sun = w.out_sun
                    shelly = Shelly(str(blind.get('device-id')))
                    if 'triggers' in blind.keys():
                        triggers = blind.get('triggers')
                    if 'in' in blind.keys():
                        in_sun = blind.get('in')
                    if 'out' in blind.keys():
                        out_sun = blind.get('out')
                    w.add_blind(Blind(blind.get('name'), in_sun, out_sun, shelly, triggers))
                walls.append(w)

    return walls


def prepare_walls() -> [Wall]:
    walls: [Wall] = []
    with open(config, 'r') as stream:
        data = yaml.safe_load(stream)
        for item in data.get('walls'):
            wall = item.get('wall')
            w = Wall(wall.get('name'), wall.get('in'), wall.get('out'))
            triggers: [] = []
            if 'blinds' in wall:
                for blind_item in wall.get('blinds'):
                    blind = blind_item.get('blind')
                    in_sun = w.in_sun
                    out_sun = w.out_sun
                    shelly = Shelly(str(blind.get('device-id')))
                    if 'triggers' in blind.keys():
                        triggers = blind.get('triggers')
                    if 'in' in blind.keys():
                        in_sun = blind.get('in')
                    if 'out' in blind.keys():
                        out_sun = blind.get('out')
                    w.add_blind(Blind(blind.get('name'), in_sun, out_sun, shelly, triggers))
                walls.append(w)

    return walls


def update_configured_devices(walls: [Wall], pool) -> [Wall]:
    updated: [Wall] = []
    for wall in walls:
        updated_blinds: [Blind] = []
        for blind in wall.blinds:
            device = blind.device
            match = device.match(pool)
            if len(match) != 1:
                logger.info('{} devices found in network for configured Device: {}'.format(len(match), device))
            else:
                if device.validate(match[0]):
                    logger.error('Device {} not configured as roller or calibrated'.format(device))
                    continue

                device.url = match[0][0]
                updated_blinds.append(blind)
        wall.blinds = updated_blinds
        if len(wall.blinds) > 0:
            updated.append(wall)
    logger.info('Updated Walls: {}'.format(updated))
    return updated


def prepare_house(devices):
    walls = prepare_walls()
    return update_configured_devices(walls, devices)
