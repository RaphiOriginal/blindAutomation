#!/usr/bin/env python3
import logging
from collections import defaultdict

import global_date
from api.api import ObservableSunAPI
from building import building
from jobs.jobmanager import manager
from pvlibrary.pvlib_api import PVLibAPI
from settings import settings
from tests.mock.mocks import SunAPIMock

logger = logging.getLogger(__name__)


def prepare_api() -> ObservableSunAPI:
    apis = defaultdict(ObservableSunAPI)
    apis['pvlib'] = PVLibAPI()
    apis['mock'] = SunAPIMock()
    return apis[settings.root.get('api')]


def main():
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')
    settings.load_settings()
    home = building.prepare()
    api: ObservableSunAPI = prepare_api()
    for blind in home.blinds:
        api.attach(blind)
    while True:
        api.fetch_sundata(global_date.date.next())
        manager.prepare().run()


main()
