import unittest

from building.blind import Blind
from building.state import State
from jobs.task import Open, PreTilt, Close
from tests.mock.device import DeviceMock


class Task(unittest.TestCase):
    def test_done_pretilt_open_state(self):
        device = DeviceMock('TestDevice')
        blind = Blind('Test', 0, 0, device, [])
        Open(blind).do()
        self.assertEqual(1, device.open_counter)
        self.assertEqual(State.OPEN, device.state)
        prepare = PreTilt(blind)
        self.assertFalse(prepare.done())

    def test_done_pretilt_close_state(self):
        device = DeviceMock('TestDevice')
        blind = Blind('Test', 0, 0, device, [])
        Close(blind).do()
        self.assertEqual(1, device.close_counter)
        self.assertEqual(State.CLOSED, device.state)
        prepare = PreTilt(blind)
        self.assertTrue(prepare.done())


if __name__ == '__main__':
    unittest.main()
