#!/usr/bin/env python3
import json
import unittest

from blind_automation.building.blind_state import BlindState, Direction
from blind_automation.building.state import State


class BlindStateCase(unittest.TestCase):

    def test_closed_state(self):
        state = BlindState(0, Direction.CLOSE)
        self.assertEqual(State.CLOSED, state.state())

    def test_tilt_close_state(self):
        state = BlindState(1, Direction.CLOSE)
        self.assertEqual(State.TILT, state.state())

    def test_tilt_open_state(self):
        state = BlindState(4, Direction.OPEN)
        self.assertEqual(State.TILT, state.state())

    def test_open_max_state(self):
        state = BlindState(100, Direction.OPEN)
        self.assertEqual(State.OPEN, state.state())

    def test_open_min_state(self):
        state = BlindState(96, Direction.OPEN)
        self.assertEqual(State.OPEN, state.state())

    def test_moved_max_open_state(self):
        state = BlindState(95, Direction.OPEN)
        self.assertEqual(State.MOVED, state.state())

    def test_moved_max_close_state(self):
        state = BlindState(100, Direction.CLOSE)
        self.assertEqual(State.MOVED, state.state())

    def test_moved_min_open_state(self):
        state = BlindState(5, Direction.OPEN)
        self.assertEqual(State.MOVED, state.state())

    def test_moved_min_close_state(self):
        state = BlindState(5, Direction.CLOSE)
        self.assertEqual(State.MOVED, state.state())

    def test_moved_zero_open_State(self):
        state = BlindState(0, Direction.OPEN)
        self.assertEqual(State.MOVED, state.state())


    def test_closed_str(self):
        state = BlindState(0, Direction.CLOSE.value)
        self.assertEqual(State.CLOSED, state.state())

    def test_tilt_close_str(self):
        state = BlindState(1, Direction.CLOSE.value)
        self.assertEqual(State.TILT, state.state())

    def test_tilt_open_str(self):
        state = BlindState(4, Direction.OPEN.value)
        self.assertEqual(State.TILT, state.state())

    def test_json(self):
        json = get_json()
        state = BlindState(json.get('current_pos'), json.get('last_direction'))
        self.assertEqual(State.CLOSED, state.state())


if __name__ == '__main__':
    unittest.main()


def get_json():
    with open('tests/mock/roller.json', 'r') as stream:
        return json.loads(stream.read())
