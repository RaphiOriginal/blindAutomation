#!/usr/bin/env python3
import logging
from collections import defaultdict

import yaml

from api.api import SunAPI
from jobs import trigger
from jobs.jobmanager import JobManager
from meteomatics.meteomatics_api import MeteomaticsAPI
from shelly import shelly_finder
from tests.mock.mocks import SunAPIMock

logger = logging.getLogger(__name__)

def prepare_api():
    apis = defaultdict(SunAPI)
    apis['meteomatics'] = MeteomaticsAPI()
    apis['mock'] = SunAPIMock()
    with open('settings.yaml', 'r') as stream:
        settings = yaml.safe_load(stream)
        return apis[settings.get('api')]

def main():
    logging.basicConfig(level=logging.DEBUG)
    shellys = shelly_finder.collect()
    api = prepare_api()
    sun = api.fetch_sundata()

    manager = JobManager()

    for shelly in shellys:
        trigger.apply_triggers(manager, sun, shelly)

    manager.prepare().run()


main()
