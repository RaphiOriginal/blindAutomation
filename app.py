#!/usr/bin/env python3
import logging
from logging import getLogger, DEBUG, INFO, WARNING, ERROR, WARN, CRITICAL, FATAL

import global_date
from building import building
from jobs.jobmanager import manager
from pvlibrary.pvlib_api import PVLibAPI
from settings import settings
from tests.mock.mocks import SunAPIMock
from weather.service import WeatherService

logger = getLogger(__name__)


class App:
    def __init__(self, setting_file: str = 'settings.yaml', logging_level: str = 'INFO'):
        settings.load_settings(setting_file)
        self.__api_pool: dict = self.__build_api_pool()
        self.__api = self.__api_pool.get(settings.root.get('api').upper())
        self.__weather_service = WeatherService()
        self.__logging_levels: dict = self.__build_logging_levels()
        self.__logging_level = self.__logging_levels.get(logging_level.upper())
        self.__home = building.prepare()
        logging.basicConfig(
            format='%(asctime)s %(levelname)-8s %(message)s',
            level=self.__logging_level,
            datefmt='%Y-%m-%d %H:%M:%S')

    def run(self):
        self.__attach_observers()
        while True:
            self.__weather_service.start()
            self.__api.fetch_sundata(global_date.date.next())
            manager.prepare().run()
            self.__weather_service.stop()

    def __attach_observers(self):
        for blind in self.__home.blinds:
            self.__api.attach(blind)
            self.__weather_service.attach(blind)

    @staticmethod
    def __build_logging_levels() -> dict:
        return {'DEBUG': DEBUG, 'INFO': INFO, 'WARNING': WARNING, 'WARN': WARN, 'ERROR': ERROR, 'CRITICAL': CRITICAL,
                'FATAL': FATAL}

    @staticmethod
    def __build_api_pool() -> dict:
        return {'PVLIB': PVLibAPI(), 'MOCK': SunAPIMock()}


def main():
    app = App()
    app.run()


main()
