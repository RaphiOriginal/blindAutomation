from building.interface import Shutter
from building.state import State
from event.event import Event


class BlindMock(Shutter):
    def __init__(self, name: str):
        self.name: str = name
        self.events: [Event] = []
        self.open_c: int = 0
        self.close_c: int = 0
        self.move_c: int = 0
        self.tilt_c: int = 0
        self.stats_c: int = 0

    def open(self) -> bool:
        self.open_c = self.open_c + 1
        return True

    def close(self) -> bool:
        pass

    def move(self, pos: int) -> bool:
        pass

    def tilt(self, degree: int) -> bool:
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

    def add_event(self, event: Event):
        self.events.append(event)

    def update(self, subject):
        for event in self.events:
            if event.applies(subject.trigger):
                event.do(self)
