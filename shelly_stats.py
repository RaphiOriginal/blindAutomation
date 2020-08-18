#!/usr/bin/env python3
import logging

import urllib3

from building import building
from settings import settings


def main():
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(name)-8s %(message)s',
        level=logging.DEBUG,
        datefmt='%Y-%m-%d %H:%M:%S')
    logging.getLogger(urllib3.__name__).setLevel(logging.WARNING)

    settings.load_settings()

    home = building.prepare()
    logging.info('{} configured and matched Walls'.format(len(home.walls)))
    for wall in home.walls:
        logging.info('On {} {} configured and matched blinds:'.format(wall.name, len(wall.blinds)))
        for blind in wall.blinds:
            logging.info('{} in position: {}'.format(blind, blind.stats()))

    logging.info("All Devices:")
    for device in home.devices:
        logging.info('{} in position {}'.format(device, device.stats()))

main()
