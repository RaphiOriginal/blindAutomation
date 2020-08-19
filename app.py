#!/usr/bin/env python3
import logging
from collections import defaultdict

import global_date
from api.api import SunAPI
from building import building
from jobs import trigger
from jobs.jobmanager import JobManager
from meteomatics.meteomatics_api import MeteomaticsAPI
from pvlibrary.pvlib_api import PVLibAPI
from settings import settings
from sun.sundata import Sundata
from tests.mock.mocks import SunAPIMock, SunAPIResponseMock

logger = logging.getLogger(__name__)


def prepare_api() -> SunAPI:
    apis = defaultdict(SunAPI)
    apis['meteomatics'] = MeteomaticsAPI()
    apis['pvlib'] = PVLibAPI()
    apis['mock'] = SunAPIMock()
    apis['responseMock'] = SunAPIResponseMock()
    return apis[settings.root.get('api')]


def main():
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')
    settings.load_settings()
    home = building.prepare()
    api: SunAPI = prepare_api()
    while True:
        sun: Sundata = api.fetch_sundata(global_date.date.next())

        manager = JobManager()

        for blind in home.blinds:
            trigger.apply_triggers(manager, sun, blind)

        if manager.prepare().run():
            break
    exit(0)


main()
