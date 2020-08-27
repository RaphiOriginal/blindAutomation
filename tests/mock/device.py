from typing import Optional

from blind_automation.building.blind.state import BlindState, Direction
from blind_automation.building.state import State
from blind_automation.device.device import Device


class DeviceMock(Device):
    def __init__(self, name: str):
        self.name: str = name
        self.blindstate: Optional[BlindState] = None
        self.state = State.UNKNOWN
        self.time: float = -1
        self.direction: str = '🤷'
        self.position: int = 100
        self.close_counter: int = 0
        self.open_counter: int = 0
        self.move_counter: int = 0
        self.tilt_counter: int = 0

    def close(self) -> bool:
        self.close_counter = self.close_counter + 1
        self.position = 0
        self.blindstate = BlindState(self.position, Direction.CLOSE)
        return True

    def open(self) -> bool:
        self.open_counter = self.open_counter + 1
        self.position = 100
        self.blindstate = BlindState(self.position, Direction.OPEN)
        return True

    def move(self, pos: int) -> bool:
        self.move_counter = self.move_counter + 1
        if pos < self.position:
            self.blindstate = BlindState(pos, Direction.CLOSE)
        else:
            self.blindstate = BlindState(pos, Direction.OPEN)
        self.position = pos
        return True

    def tilt(self, direction: str, time: float) -> bool:
        self.time = time
        self.direction = direction
        self.tilt_counter = self.tilt_counter + 1
        self.position = 2
        self.blindstate = BlindState(self.position, Direction.from_name(direction))
        return True

    def stats(self) -> State:
        if self.blindstate:
            self.state = self.blindstate.state()
        return self.state

    def id(self) -> str:
        return self.name

    def __repr__(self):
        return 'DeviceMock: {name: %s, close: %s, open: %s, move: %s, tilt: %s}' % \
               (self.name, self.close_counter, self.open_counter, self.move_counter, self.tilt_counter)
