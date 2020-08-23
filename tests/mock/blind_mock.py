from typing import List, Optional

from building.interface import Shutter
from building.state import State
from event.event import Event, Blocker


class BlindMock(Shutter):
    def __init__(self, name: str):
        self.name: str = name
        self.blocker: Optional[Blocker] = None
        self.events: [Event] = []
        self.open_c: int = 0
        self.close_c: int = 0
        self.move_c: int = 0
        self.tilt_c: int = 0
        self.stats_c: int = 0

    def open(self) -> Optional[Blocker]:
        if self.blocker is None or not self.blocker.blocking:
            self.open_c = self.open_c + 1
        return self.blocker

    def close(self) -> Optional[Blocker]:
        pass

    def move(self, pos: int) -> Optional[Blocker]:
        pass

    def tilt(self, degree: int) -> Optional[Blocker]:
        pass

    def stats(self) -> State:
        pass

    @property
    def id(self) -> str:
        return self.name

    def name(self) -> str:
        return self.name

    def sun_in(self) -> float:
        pass

    def sun_out(self) -> float:
        pass

    def triggers(self) -> []:
        pass

    def degree(self) -> int:
        pass

    def overwrite_degree(self, degree: int):
        pass

    def event_configs(self) -> List:
        pass

    def add_events(self, events: [Event]):
        self.events = events

    def update(self, subject):
        for event in self.events:
            if event.applies(subject.trigger):
                self.blocker = event.do(self)
