import unittest

from blinds.blind_state import Direction, BlindState, State


class BlindStateCase(unittest.TestCase):

    def test_closed_state(self):
        state = BlindState(0, Direction.CLOSE)
        self.assertEqual(State.CLOSED, state.state())

    def test_open_state(self):
        state = BlindState(1, Direction.CLOSE)
        self.assertEqual(State.OPEN, state.state())

    def test_tilt_state(self):
        state = BlindState(4, Direction.OPEN)
        self.assertEqual(State.TILT, state.state())

    def test_closed_str(self):
        state = BlindState(0, Direction.CLOSE.value)
        self.assertEqual(State.CLOSED, state.state())

    def test_open_str(self):
        state = BlindState(1, Direction.CLOSE.value)
        self.assertEqual(State.OPEN, state.state())

    def test_tilt_str(self):
        state = BlindState(4, Direction.OPEN.value)
        self.assertEqual(State.TILT, state.state())


if __name__ == '__main__':
    unittest.main()
