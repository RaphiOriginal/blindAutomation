from abc import ABC, abstractmethod
from typing import Any


class Event(ABC):

    @abstractmethod
    def applies(self, trigger: Any) -> bool:
        """
        Check if the Event applies. Always typecheck the trigger it could by anything!
        :param trigger: object that could trigger an event
        :return: True if event applies
        """
        pass

    @abstractmethod
    def do(self, on: Any) -> bool:
        """
        Execute the event
        :param on: Blinds to be moved
        :return: True if event was Successfully executed
        """