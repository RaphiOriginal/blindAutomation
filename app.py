#!/usr/bin/env python3
import logging
from collections import defaultdict

import yaml

from api.api import SunAPI
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
    logging.basicConfig(level=logging.DEBUG)
    shellys = shelly_finder.collect()
    if len(shellys) > 0:
        api: SunAPI = prepare_api()
        sun: Sundata = api.fetch_sundata()

        manager = JobManager()

        for shelly in shellys:
            trigger.apply_triggers(manager, sun, shelly)

        manager.prepare().run()
    else:
        logger.info('No configured shellys found')


main()
