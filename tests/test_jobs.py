import unittest

from building.blind import Blind
from building.state import State
from device.device import Device
from jobs.jobmanager import manager
from tests.mock.mocks import SunAPIMock


class ParallelBlindsCase(unittest.TestCase):
    def test_parallel_tasks(self):
        blinds = [
            Blind('A', 0, 0, TestDevice('A'), ['SUNRISE']),
            Blind('B', 0, 0, TestDevice('B'), ['SUNRISE'])
        ]
        api = SunAPIMock()
        for blind in blinds:
            api.attach(blind)
        api.fetch_sundata(None)
        manager.prepare().run()
        self.assertEqual(1, blinds[0].device.counter, "A was called")
        self.assertEqual(1, blinds[1].device.counter, "B was called")


class TestDevice(Device):
    def __init__(self, id: str):
        self.__id = id
        self.counter = 0

    def close(self) -> bool:
        return False

    def open(self) -> bool:
        self.counter = self.counter + 1
        return True

    def move(self, pos: int) -> bool:
        return False

    def tilt(self, direction: str, time: float) -> bool:
        return True

    def stats(self) -> State:
        return True

    def id(self) -> str:
        return self.__id


if __name__ == '__main__':
    unittest.main()
