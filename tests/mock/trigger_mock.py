from event.trigger import Trigger
from observable.observable import Subject, Observer
from weather.weather import Weather


class TriggerMock(Subject, Trigger):
    def __init__(self, trigger: Weather):
        self._trigger = trigger

    def attach(self, observer: Observer):
        pass

    def detach(self, observer: Observer):
        pass

    def notify(self):
        pass

    @property
    def trigger(self) -> Weather:
        return self._trigger
