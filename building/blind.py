#!/usr/bin/env python3
from typing import List, Optional

from api.api import ObservableSunAPI
from building.interface import Shutter
from building.state import State
from device.device import Device
from event.event import Event, Blocker
from event.trigger import Trigger
from jobs import trigger
from jobs.jobmanager import manager
from observable.observable import Subject


class Blind(Shutter):
    def __init__(self, name: str, sun_in: float, sun_out: float, device: Device, triggers: [], event_config: []):
        self._name: str = name
        self._sun_in: float = sun_in
        self._sun_out: float = sun_out
        self.device: Device = device
        self._triggers: [] = triggers
        self._event_config: [] = event_config
        self._events: [Event] = []
        self.state: State = State.UNKNOWN
        self.__degree: int = -1
        self.__duration: float = 1.2
        self.__blocker: Optional[Blocker] = None

    def open(self) -> Optional[Blocker]:
        if self.__not_blocking():
            self.__degree = 0
            self.device.open()
        return self.__blocker

    def close(self) -> Optional[Blocker]:
        if self.__not_blocking():
            self.__degree = 90
            self.device.close()
        return self.__blocker

    def move(self, pos: int) -> Optional[Blocker]:
        if self.__not_blocking():
            self.device.move(pos)
        return self.__blocker

    def tilt(self, degree: int) -> Optional[Blocker]:
        if self.__not_blocking():
            target = min(max(degree, 0), 90)
            offset = target - self.__degree
            duration = abs(self.__duration / 90 * offset)
            self.__degree = target
            if offset > 0:
                self.device.tilt('close', duration)
            else:
                self.device.tilt('open', duration)
        return self.__blocker

    def stats(self) -> State:
        self.state = self.device.stats()
        return self.state

    def override_tilt_duration(self, duration):
        self.__duration = duration

    def overwrite_degree(self, degree: int):
        self.__degree = degree

    def add_events(self, events: [Event]):
        for event in events:
            self._events.append(event)

    @property
    def events(self) -> [Event]:
        return self._events

    @property
    def id(self):
        return self.device.id

    @property
    def degree(self) -> int:
        return self.__degree

    @property
    def name(self) -> str:
        return self._name

    @property
    def sun_in(self) -> float:
        return self._sun_in

    @property
    def sun_out(self) -> float:
        return self._sun_out

    @property
    def triggers(self) -> List:
        return self._triggers

    @property
    def event_configs(self) -> List:
        return self._event_config

    def update(self, subject: Subject):
        if isinstance(subject, ObservableSunAPI):
            trigger.apply_triggers(manager, subject.sundata, self)
        if isinstance(subject, Trigger):
            for event in self._events:
                if event.applies(subject.trigger):
                    event.do(self)

    def __not_blocking(self) -> bool:
        return self.__blocker is None or not self.__blocker.blocking

    def __repr__(self):
        return 'Blind: { name: %s, sun_in: %s, sun_out: %s, device: %s, events: %s, triggers: %s, state: %s, event_config: %s}' \
               % (self.name, self.sun_in, self.sun_out, self.device, self._events, self.triggers, self.state, self._event_config)
