#!/usr/bin/env python3
import logging

from yamale import yamale

from building import building
from shelly import shelly_finder


def main():
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.DEBUG,
        datefmt='%Y-%m-%d %H:%M:%S')

    schema = yamale.make_schema('schema.yaml')
    data = yamale.make_data('settings.yaml')
    yamale.validate(schema, data)

    devices = shelly_finder.collect_devices()
    walls = building.prepare_house(devices)
    logging.info('{} configured and matched Walls'.format(len(walls)))
    for wall in walls:
        logging.info('On {} {} configured and matched blinds:'.format(wall.name, len(wall.blinds)))
        for blind in wall.blinds:
            logging.info(blind.device)


main()
