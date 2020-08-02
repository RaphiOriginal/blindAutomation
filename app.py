#!/usr/bin/env python3
import logging
from collections import defaultdict

import yaml
from yamale import yamale

from api.api import SunAPI
from building import building
from jobs import trigger
from jobs.jobmanager import JobManager
from meteomatics.meteomatics_api import MeteomaticsAPI
from shelly import shelly_finder
from sun.sundata import Sundata
from tests.mock.mocks import SunAPIMock, SunAPIResponseMock

logger = logging.getLogger(__name__)


def prepare_api() -> SunAPI:
    apis = defaultdict(SunAPI)
    apis['meteomatics'] = MeteomaticsAPI()
    apis['mock'] = SunAPIMock()
    apis['responseMock'] = SunAPIResponseMock()
    with open('settings.yaml', 'r') as stream:
        settings = yaml.safe_load(stream)
        return apis[settings.get('api')]


def main():
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')
    validate_settings()
    devices = shelly_finder.collect_devices()
    walls = building.prepare_house(devices)
    if len(walls) > 0:
        api: SunAPI = prepare_api()
        sun: Sundata = api.fetch_sundata()

        manager = JobManager()

        for wall in walls:
            for blind in wall.blinds:
                trigger.apply_triggers(manager, sun, blind)

        manager.prepare().run()
        exit(0)
    else:
        logger.info('No configured shellys found')
        exit(1)


def validate_settings():
    schema = yamale.make_schema('schema.yaml')
    data = yamale.make_data('settings.yaml')
    yamale.validate(schema, data)


main()
