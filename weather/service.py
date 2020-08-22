#!/usr/bin/env python3
import logging
from threading import Thread, Event
from typing import Optional

from building.interface import Shutter
from event.trigger import Trigger
from observable.observable import Subject, Observer
from settings import settings
from weather import event
from weather.api import OpenWeatherAPI
from weather.interface import WeatherAPI
from weather.weather import Weather

logger = logging.getLogger(__name__)


class WeatherService(Subject, Trigger):

    def __init__(self, api: Optional[WeatherAPI] = None, interval: int = 180):
        self.__observers: [Observer] = []
        self.__current: Optional[Weather] = None
        self.__api: WeatherAPI = OpenWeatherAPI(settings.coordinates)
        if api:
            self.__api = api
        self.__event: Event = Event()
        self.__interval: int = interval  # in seconds
        self.__thread: Optional[Thread] = None
        self.__history: [Weather] = []

    def attach(self, observer: Observer):
        logger.debug('Adding observer {}'.format(observer))
        if isinstance(observer, Shutter):
            event.apply_weather_events(observer)
            logger.info('Adding Events to {}: {}'.format(observer.name, observer.events))
        self.__observers.append(observer)

    def detach(self, observer: Observer):
        logger.debug('Removing observer {}'.format(observer))
        self.__observers.remove(observer)

    def notify(self):
        if self.__current:
            logger.debug('Notifying observers: {}'.format(self.__observers))
            for observer in self.__observers:
                observer.update(self)

    def stop(self):
        logger.debug('Stopping service')
        self.__event.set()
        if self.__thread and self.__thread.is_alive():
            self.__thread.join()
        logger.info('Service stopped')

    def start(self):
        logger.debug('Starting service')
        self.__history = []
        self.__event.clear()
        self.__thread = Thread(target=self.run, daemon=True)
        self.__thread.start()
        logger.info('Service started')

    def run(self):
        while not self.__event.is_set():
            weather = self.__api.fetch_current()
            self.__update_current(weather)
            self.__event.wait(self.__interval)
        logger.debug('Leaving service loop')

    @property
    def current(self) -> Optional[Weather]:
        return self.__current

    @property
    def trigger(self) -> Optional[Weather]:
        return self.current

    def __update_current(self, new: Optional[Weather]):
        if self.__current:
            self.__history.append(self.__current)
        logger.debug('Updating current: {} with: {}'.format(self.__current, new))
        self.__current = new
        self.notify()

    def __repr__(self):
        return 'WeatherService: {running: %s, interval: %s, current: %s, history: %s, api: %s}' % \
               (not self.__event.is_set(), self.__interval, self.__current, self.__history, self.__api)
