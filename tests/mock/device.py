from building.state import State
from device.device import Device


class DeviceMock(Device):
    def __init__(self, name: str):
        self.name: str = name
        self.state: State = State.UNKNOWN
        self.time: float = -1
        self.close_counter: int = 0
        self.open_counter: int = 0
        self.move_counter: int = 0
        self.tilt_counter: int = 0

    def close(self) -> bool:
        self.close_counter = self.close_counter + 1
        self.state = State.CLOSED
        return True

    def open(self) -> bool:
        self.open_counter = self.open_counter + 1
        self.state = State.OPEN
        return True

    def move(self, pos: int) -> bool:
        self.move_counter = self.move_counter + 1
        return True

    def tilt(self, direction: str, time: float) -> bool:
        self.time = time
        self.tilt_counter = self.tilt_counter + 1
        self.state = State.TILT
        return True

    def stats(self) -> State:
        return self.state

    def id(self) -> str:
        return self.name

    def __repr__(self):
        return 'DeviceMock: {name: %s, close: %s, open: %s, move: %s, tilt: %s}' % \
               (self.name, self.close_counter, self.open_counter, self.move_counter, self.tilt_counter)
