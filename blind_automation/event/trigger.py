#!/usr/bin/env python3
from abc import ABC, abstractmethod
from typing import Any


class Trigger(ABC):

    @property
    @abstractmethod
    def trigger(self) -> Any:
        """
        Returns the subject of matter to check a event trigger.
        The event then has to typecheck it for himself!
        :return: Anything that possibly can trigger an event
        """
        pass
