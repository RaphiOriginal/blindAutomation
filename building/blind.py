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

    def open(self) -> bool:
        return self.device.open()

    def close(self) -> bool:
        return self.device.close()

    def move(self, pos: int) -> bool:
        return self.device.move(pos)

    def stats(self) -> State:
        self.state = self.device.stats()
        return self.state

    @property
    def id(self):
        return self.device.id

    def __repr__(self):
        return 'Blind: { name: %s, sun_in: %s, sun_out: %s, device: %s, triggers: %s, state: %s }' % \
               (self.name, self.sun_in, self.sun_out, self.device, self.triggers, self.state)
