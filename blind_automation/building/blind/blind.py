#!/usr/bin/env python3
from typing import List, Optional

from blind_automation.api.api import ObservableSunAPI
from blind_automation.building.interface import Shutter
from blind_automation.building.state import State
from blind_automation.device.device import Device
from blind_automation.event.blocker import Blocker
from blind_automation.event.event import Event
from blind_automation.event.trigger import Trigger
from blind_automation.jobs import trigger
from blind_automation.jobs.jobmanager import manager
from blind_automation.observable.observable import Subject


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
        self.__degree: int = 90
        self.__duration: float = 1.2
        self._blocker: Blocker = Blocker()

    def open(self) -> Optional[Blocker]:
        if self.__not_blocking():
            self.__degree = 0
            self.device.open()
        return self._blocker

    def close(self) -> Optional[Blocker]:
        if self.__not_blocking():
            self.__degree = 90
            self.device.close()
        return self._blocker

    def move(self, pos: int) -> Optional[Blocker]:
        if self.__not_blocking():
            self.device.move(pos)
        return self._blocker

    def tilt(self, degree: int) -> Optional[Blocker]:
        if self.state == State.UNKNOWN:
            self.stats()
        if self.__not_blocking():
            target = min(max(degree, 0), 90)
            offset = target - self.__degree
            duration = abs(self.__duration / 90 * offset)
            self.__degree = target
            if offset >= 0:
                self.device.tilt('close', duration)
            else:
                self.device.tilt('open', duration)
        return self._blocker

    def stats(self) -> State:
        self.state = self.device.stats()
        if State.CLOSED == self.state:
            self.__degree = 90
        if State.OPEN == self.state:
            self.__degree = 0
        if State.TILT == self.state and self.__degree == 90:
            self.__degree = 0
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
        self._events.sort(key=lambda event: not event.active)
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

    @property
    def blocked(self) -> bool:
        if self._blocker:
            return self._blocker.blocking
        return False

    @property
    def blocker(self) -> Blocker:
        return self._blocker

    def update(self, subject: Subject):
        if isinstance(subject, ObservableSunAPI):
            trigger.apply_triggers(manager, subject.sundata, self)
        if isinstance(subject, Trigger):
            for event in self.events:
                if event.applies(subject.trigger, self):
                    event.do(self)

    def __not_blocking(self) -> bool:
        return self._blocker is None or not self._blocker.blocking

    def __repr__(self):
        return 'Blind: { name: %s, sun_in: %s, sun_out: %s, device: %s, events: %s, triggers: %s, state: %s, ' \
               'degree: %s, event_config: %s}' \
               % (self.name, self.sun_in, self.sun_out, self.device, self._events, self.triggers, self.state,
                  self.__degree, self._event_config)
