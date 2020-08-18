#!/usr/bin/env python3
import logging

from building import building
from settings import settings


def main():
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.DEBUG,
        datefmt='%Y-%m-%d %H:%M:%S')

    settings.load_settings()

    home = building.prepare()
    logging.info('{} configured and matched Walls'.format(len(home.walls)))
    for wall in home.walls:
        logging.info('On {} {} configured and matched blinds:'.format(wall.name, len(wall.blinds)))
        logging.info(wall.devices)

    logging.info("All Devices:")
    for device in home.devices:
        logging.info(device)

main()
