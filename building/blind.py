from api.api import ObservableSunAPI
from building.blind_interface import BlindInterface
from building.state import State
from device.device import Device
from jobs import trigger
from jobs.jobmanager import manager


class Blind(BlindInterface):
    def __init__(self, name: str, sun_in: float, sun_out: float, device: Device, triggers: []):
        self._name: str = name
        self._sun_in: float = sun_in
        self._sun_out: float = sun_out
        self.device: Device = device
        self._triggers: [] = triggers
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

    def overwrite_degree(self, degree: int):
        self.__degree = degree

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
    def triggers(self) -> []:
        return self._triggers

    def update(self, api: ObservableSunAPI):
        trigger.apply_triggers(manager, api.sundata, self)

    def __repr__(self):
        return 'Blind: { name: %s, sun_in: %s, sun_out: %s, device: %s, triggers: %s, state: %s }' % \
               (self.name, self.sun_in, self.sun_out, self.device, self.triggers, self.state)
