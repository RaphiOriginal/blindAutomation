from building.state import State
from device.device import Device


class Blind:
    def __init__(self, name: str, sun_in: float, sun_out: float, device: Device, triggers: []):
        self.name: str = name
        self.sun_in: float = sun_in
        self.sun_out: float = sun_out
        self.device: Device = device
        self.triggers: [] = triggers
        self.state: State = State.UNKNOWN
        self.__degree: int = -1
        self.__duration: float = 1.2

    def open(self) -> bool:
        self.__degree = 0
        return self.device.open()

    def close(self) -> bool:
        self.__degree = 90
        return self.device.close()

    def move(self, pos: int) -> bool:
        return self.device.move(pos)

    def tilt(self, degree: int) -> bool:
        target = min(max(degree, 0), 90)
        offset = target - self.__degree
        duration = abs(self.__duration / 90 * offset)
        self.__degree = target
        if offset > 0:
            return self.device.tilt('close', duration)
        else:
            return self.device.tilt('open', duration)

    def stats(self) -> State:
        self.state = self.device.stats()
        return self.state

    def override_tilt_duration(self, duration):
        self.__duration = duration

    @property
    def id(self):
        return self.device.id

    @property
    def degree(self) -> int:
        return self.__degree

    def __repr__(self):
        return 'Blind: { name: %s, sun_in: %s, sun_out: %s, device: %s, triggers: %s, state: %s }' % \
               (self.name, self.sun_in, self.sun_out, self.device, self.triggers, self.state)
