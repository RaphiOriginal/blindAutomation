#!/usr/bin/env python3
import logging

from yamale import yamale

from shelly import shelly_finder


def main():
    logging.basicConfig(level=logging.INFO)

    schema = yamale.make_schema('schema.yaml')
    data = yamale.make_data('settings.yaml')
    yamale.validate(schema, data)

    walls = shelly_finder.collect()
    logging.info('{} configured and matched Walls'.format(len(walls)))
    for wall in walls:
        logging.info('On {} {} configured and matched blinds:'.format(wall.name, len(wall.blinds)))
        for blind in wall.blinds:
            logging.info(blind.shelly)


main()
