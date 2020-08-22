from abc import ABC, abstractmethod

from weather.weather import Weather


class Event(ABC):

    @abstractmethod
    def applies(self, weather: Weather) -> bool:
        """
        Check if the Event applies
        :return: True if event applies
        """
        pass

    @abstractmethod
    def do(self) -> bool:
        """
        Execute the event
        :return: True if event was Successfully executed
        """