#!/usr/bin/env python3
import logging
from logging import getLogger, DEBUG, INFO, WARNING, ERROR, CRITICAL, FATAL

import global_date
from api.api import ObservableSunAPI
from building import building
from jobs.jobmanager import manager
from pvlibrary.pvlib_api import PVLibAPI
from settings import settings
from tests.mock.mocks import SunAPIMock
from weather.service import WeatherService

logger = getLogger(__name__)


class App:
    def __init__(self, setting_file: str = 'settings.yaml', log: str = 'INFO'):
        settings.load_settings(setting_file)
        self._api = self.__api(settings.root.get('api'))
        self._weather_service = WeatherService()
        self._level = self.__level(log)
        self.__home = building.prepare()

    def run(self):
        logging.basicConfig(
            format='%(asctime)s %(levelname)-8s %(message)s',
            level=self._level,
            datefmt='%Y-%m-%d %H:%M:%S')
        self.__attach_observers()
        while True:
            self._weather_service.start()
            self._api.fetch_sundata(global_date.date.next())
            manager.prepare().run()
            self._weather_service.stop()

    def __attach_observers(self):
        for blind in self.__home.blinds:
            self._api.attach(blind)
            self._weather_service.attach(blind)

    @staticmethod
    def __level(level: str) -> int:
        return {'DEBUG': DEBUG, 'INFO': INFO, 'WARNING': WARNING, 'ERROR': ERROR, 'CRITICAL': CRITICAL,
                'FATAL': FATAL}[level.upper()]

    @staticmethod
    def __api(api: str) -> ObservableSunAPI:
        return {'PVLIB': PVLibAPI(), 'MOCK': SunAPIMock()}[api.upper()]


def main():
    app = App()
    app.run()


main()
