import unittest

from blind_automation.building.blind.blind import Blind
from blind_automation.building.state import State
from tests.mock.device import DeviceMock


class BlindDegreeCase(unittest.TestCase):
    def test_tilt_calculation_initial(self):
        mock = DeviceMock('👨‍🏫')
        blind = Blind('👨‍🎓', 10, 20, mock, [], [])
        blind.override_tilt_duration(90)  # Makes calculation for checks much more easy =)
        # starting from 90
        blind.tilt(0)
        self.assertEqual(90, mock.time)
        self.assertEqual('open', mock.direction)

    def test_tilt_calculation_open(self):
        mock = DeviceMock('👨‍🏫')
        blind = Blind('👨‍🎓', 10, 20, mock, [], [])
        blind.override_tilt_duration(90)  # Makes calculation for checks much more easy =)
        blind.open()
        self.assertEqual(State.OPEN, mock.stats())
        blind.tilt(0)
        self.assertEqual(0, mock.time)
        self.assertEqual('close', mock.direction)

    def test_tilt_calculation_close(self):
        mock = DeviceMock('👨‍🏫')
        blind = Blind('👨‍🎓', 10, 20, mock, [], [])
        blind.override_tilt_duration(90)  # Makes calculation for checks much more easy =)
        blind.close()
        self.assertEqual(State.CLOSED, mock.stats())
        blind.tilt(0)
        self.assertEqual(90, mock.time)
        self.assertEqual('open', mock.direction)

    def test_tilt_calculation_45(self):
        mock = DeviceMock('👨‍🏫')
        blind = Blind('👨‍🎓', 10, 20, mock, [], [])
        blind.override_tilt_duration(90)  # Makes calculation for checks much more easy =)
        # starting from 90
        blind.tilt(45)
        self.assertEqual(45, mock.time)
        self.assertEqual('open', mock.direction)

    def test_tilt_calculation_90(self):
        mock = DeviceMock('👨‍🏫')
        blind = Blind('👨‍🎓', 10, 20, mock, [], [])
        blind.override_tilt_duration(90)  # Makes calculation for checks much more easy =)
        # starting from 90
        blind.tilt(90)
        self.assertEqual(0, mock.time)
        self.assertEqual('close', mock.direction)

    def test_tilt_calculation_30_60(self):
        mock = DeviceMock('👨‍🏫')
        blind = Blind('👨‍🎓', 10, 20, mock, [], [])
        blind.override_tilt_duration(90)  # Makes calculation for checks much more easy =)
        # starting from 90
        blind.tilt(30)
        self.assertEqual(60, mock.time)
        self.assertEqual('open', mock.direction)
        blind.tilt(60)
        self.assertEqual(30, mock.time)
        self.assertEqual('close', mock.direction)

    def test_tilt_calculation_60_30(self):
        mock = DeviceMock('👨‍🏫')
        blind = Blind('👨‍🎓', 10, 20, mock, [], [])
        blind.override_tilt_duration(90)  # Makes calculation for checks much more easy =)
        # starting from 90
        blind.tilt(60)
        self.assertEqual(30, mock.time)
        self.assertEqual('open', mock.direction)
        blind.tilt(30)
        self.assertEqual(30, mock.time)
        self.assertEqual('open', mock.direction)


if __name__ == '__main__':
    unittest.main()
