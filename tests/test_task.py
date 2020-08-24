import unittest

from building.blind import Blind
from building.state import State
from jobs.task import Open, PreTilt, Close, Tilt
from tests.mock.device import DeviceMock


class Task(unittest.TestCase):
    def test_done_pretilt_open_state(self):
        device = DeviceMock('TestDevice')
        blind = Blind('Test', 0, 0, device, [])
        Open(blind).do()
        self.assertEqual(1, device.open_counter)
        self.assertEqual(State.OPEN, device.stats())
        prepare = PreTilt(blind)
        self.assertFalse(prepare.done())

    def test_done_pretilt_close_state(self):
        device = DeviceMock('TestDevice')
        blind = Blind('Test', 0, 0, device, [])
        Close(blind).do()
        self.assertEqual(1, device.close_counter)
        self.assertEqual(State.CLOSED, device.stats())
        prepare = PreTilt(blind)
        self.assertTrue(prepare.done())

    def test_done_pretilt_tilt_state(self):
        device = DeviceMock('TestDevice')
        blind = Blind('Test', 0, 0, device, [])
        Tilt(blind).do()
        self.assertEqual(1, device.tilt_counter)
        self.assertEqual(State.TILT, device.stats())
        prepare = PreTilt(blind)
        self.assertTrue(prepare.done())

    def test_done_pretilt_moved_state(self):
        device = DeviceMock('TestDevice')
        blind = Blind('Test', 0, 0, device, [])
        device.move(50)
        prepare = PreTilt(blind)
        self.assertFalse(prepare.done())

    def test_done_tilt_open_state(self):
        device = DeviceMock('TestDevice')
        blind = Blind('Test', 0, 0, device, [])
        Open(blind).do()
        self.assertEqual(1, device.open_counter)
        self.assertEqual(State.OPEN, device.stats())
        tilt = Tilt(blind)
        self.assertFalse(tilt.done())

    def test_done_tilt_close_state(self):
        device = DeviceMock('TestDevice')
        blind = Blind('Test', 0, 0, device, [])
        Close(blind).do()
        self.assertEqual(1, device.close_counter)
        self.assertEqual(State.CLOSED, device.stats())
        tilt = Tilt(blind)
        self.assertFalse(tilt.done())

    def test_done_tilt_tilt_state(self):
        device = DeviceMock('TestDevice')
        blind = Blind('Test', 0, 0, device, [])
        Tilt(blind).do()
        self.assertEqual(1, device.tilt_counter)
        self.assertEqual(State.TILT, device.stats())
        tilt = Tilt(blind)
        self.assertTrue(tilt.done())

    def test_done_tilt_different_tilt_state(self):
        device = DeviceMock('TestDevice')
        blind = Blind('Test', 0, 0, device, [])
        Tilt(blind, 45).do()
        self.assertEqual(1, device.tilt_counter)
        self.assertEqual(State.TILT, device.stats())
        tilt = Tilt(blind)
        self.assertFalse(tilt.done())

    def test_done_tilt_moved_state(self):
        device = DeviceMock('TestDevice')
        blind = Blind('Test', 0, 0, device, [])
        device.move(50)
        tilt = Tilt(blind)
        self.assertFalse(tilt.done())

    def test_done_close_open_state(self):
        device = DeviceMock('TestDevice')
        blind = Blind('Test', 0, 0, device, [])
        Open(blind).do()
        self.assertEqual(1, device.open_counter)
        self.assertEqual(State.OPEN, device.stats())
        close = Close(blind)
        self.assertFalse(close.done())

    def test_done_close_close_state(self):
        device = DeviceMock('TestDevice')
        blind = Blind('Test', 0, 0, device, [])
        Close(blind).do()
        self.assertEqual(1, device.close_counter)
        self.assertEqual(State.CLOSED, device.stats())
        close = Close(blind)
        self.assertTrue(close.done())

    def test_done_close_tilt_state(self):
        device = DeviceMock('TestDevice')
        blind = Blind('Test', 0, 0, device, [])
        Tilt(blind).do()
        self.assertEqual(1, device.tilt_counter)
        self.assertEqual(State.TILT, device.stats())
        close = Close(blind)
        self.assertFalse(close.done())

    def test_done_close_moved_state(self):
        device = DeviceMock('TestDevice')
        blind = Blind('Test', 0, 0, device, [])
        device.move(50)
        close = Close(blind)
        self.assertFalse(close.done())

    def test_done_open_open_state(self):
        device = DeviceMock('TestDevice')
        blind = Blind('Test', 0, 0, device, [])
        Open(blind).do()
        self.assertEqual(1, device.open_counter)
        self.assertEqual(State.OPEN, device.stats())
        task = Open(blind)
        self.assertTrue(task.done())

    def test_done_open_close_state(self):
        device = DeviceMock('TestDevice')
        blind = Blind('Test', 0, 0, device, [])
        Close(blind).do()
        self.assertEqual(1, device.close_counter)
        self.assertEqual(State.CLOSED, device.stats())
        task = Open(blind)
        self.assertFalse(task.done())

    def test_done_open_tilt_state(self):
        device = DeviceMock('TestDevice')
        blind = Blind('Test', 0, 0, device, [])
        Tilt(blind).do()
        self.assertEqual(1, device.tilt_counter)
        self.assertEqual(State.TILT, device.stats())
        task = Open(blind)
        self.assertFalse(task.done())

    def test_done_open_moved_state(self):
        device = DeviceMock('TestDevice')
        blind = Blind('Test', 0, 0, device, [])
        device.move(50)
        task = Open(blind)
        self.assertFalse(task.done())


if __name__ == '__main__':
    unittest.main()
