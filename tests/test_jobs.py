import unittest

from building.blind import Blind
from building.state import State
from device.device import Device
from jobs import trigger
from jobs.job import Job
from jobs.jobmanager import manager
from jobs.task import Open
from jobs.trigger import SunriseTrigger
from tests.mock import mocks
from tests.mock.mocks import SunAPIMock


class ParallelBlindsCase(unittest.TestCase):
    def test_parallel_tasks_triggers_extract(self):
        blinds = [
            Blind('A', 0, 0, TestDevice('A'), ['SUNRISE']),
            Blind('B', 0, 0, TestDevice('B'), ['SUNRISE'])
        ]
        api = SunAPIMock()
        api.fetch_sundata(None)
        for blind in blinds:
            triggers = trigger.extract_triggers(blind, api.sundata)
            print(triggers)
            manager.add(Job(triggers[0], blind))
        print(manager)
        manager.prepare()
        print(manager)
        manager.run()
        self.assertEqual(1, blinds[1].device.counter, '{} was called'.format(blinds[1].name))
        self.assertEqual(1, blinds[0].device.counter, '{} was called'.format(blinds[0].name))

    def test_parallel_tasks_directly(self):
        device_a = TestDevice('A')
        device_b = TestDevice('B')
        manager.add(Job(SunriseTrigger(mocks.get_sundata_mock(), Open()), Blind('A', 0, 0, device_a, ['SUNRISE'])))
        manager.add(Job(SunriseTrigger(mocks.get_sundata_mock(), Open()), Blind('B', 0, 0, device_b, ['SUNRISE'])))
        manager.prepare().run()
        self.assertEqual(1, device_b.counter, 'B was called')
        self.assertEqual(1, device_a.counter, 'A was called')


class TestDevice(Device):
    def __init__(self, id: str):
        self.__id = id
        self.counter = 0

    def close(self) -> bool:
        return False

    def open(self) -> bool:
        self.counter = self.counter + 1
        print('open {}'.format(self.id))
        return True

    def move(self, pos: int) -> bool:
        return False

    def tilt(self, direction: str, time: float) -> bool:
        return True

    def stats(self) -> State:
        return True

    @property
    def id(self) -> str:
        return self.__id

    def __repr__(self):
        return self.__id


if __name__ == '__main__':
    unittest.main()
