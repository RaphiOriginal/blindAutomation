from blind_automation.event.trigger import Trigger
from blind_automation.observable.observable import Subject, Observer
from blind_automation.weather.weather import Weather


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
