#!/usr/bin/env python3
import logging
from collections import defaultdict
from datetime import datetime, timedelta

from dateutil.tz import tz

from api.api import SunAPI
from building import building
from jobs import trigger
from jobs.jobmanager import JobManager
from meteomatics.meteomatics_api import MeteomaticsAPI
from settings import settings
from shelly import shelly_finder
from sun.sundata import Sundata
from tests.mock.mocks import SunAPIMock, SunAPIResponseMock

logger = logging.getLogger(__name__)


def prepare_api() -> SunAPI:
    apis = defaultdict(SunAPI)
    apis['meteomatics'] = MeteomaticsAPI()
    apis['mock'] = SunAPIMock()
    apis['responseMock'] = SunAPIResponseMock()
    return apis[settings.root.get('api')]


def main():
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')
    settings.load_settings()
    devices = shelly_finder.collect_devices()
    walls = building.prepare_house(devices)
    if len(walls) > 0:
        api: SunAPI = prepare_api()
        now = datetime.now(tz.tzlocal())
        while True:
            sun: Sundata = api.fetch_sundata(now)
            now = now + timedelta(days=1)

            manager = JobManager()

            for wall in walls:
                for blind in wall.blinds:
                    trigger.apply_triggers(manager, sun, blind)

            if manager.prepare().run():
                break
        exit(0)
    else:
        logger.info('No configured shellys found')
        exit(1)


main()
