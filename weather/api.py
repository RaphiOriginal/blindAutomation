import logging
import os
from typing import Optional

import requests

from settings import settings
from weather.weather import Weather

logger = logging.getLogger(__name__)


class OpenWeatherAPI:
    def __init__(self, units: str = 'metric', lang: str = 'de'):
        self.__units: str = units
        self.__lang: str = lang
        self.__base_url: str = 'https://api.openweathermap.org/data/2.5/{}'
        self.__current_template: str = 'weather?lat={}&lon={}&units={}&lang={}&appid={}'
        self.__coordinates = settings.coordinates

    def fetch_current(self) -> Optional[Weather]:
        url = self.__build_current_url()
        response = requests.get(url)
        if response.status_code != 200:
            logger.error('Call {} failed with status {} and content: {}'.format(url, response.status_code, response.text))
            return None
        else:
            logger.debug('Successfully received {} with {}'.format(response.text, url))
            return Weather(response.json())

    def __build_current_url(self) -> str:
        key = os.getenv('OPEN_WEATHER_API_KEY')
        parameters = self.__current_template.format(self.__coordinates.lat, self.__coordinates.long, self.__units,
                                                    self.__lang, key)
        return self.__base_url.format(parameters)

    def __repr__(self):
        return 'OpenWeatherApi: {units: %s, language: %s, url: %s, %s}' % \
               (self.__units, self.__lang, self.__base_url, self.__coordinates)
