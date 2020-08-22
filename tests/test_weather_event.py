import json
import unittest

from tests.mock.blind_mock import BlindMock
from tests.mock.trigger_mock import TriggerMock
from weather.event import CloudsEvent, WeatherEvent
from weather.weather import Weather


class WeatherEventCase(unittest.TestCase):
    def test_clouds(self):
        # Setup
        event = CloudsEvent()
        blind, trigger = self.__prepare(event, 804)
        # Test
        blind.update(trigger)
        # Check
        self.assertEqual(1, blind.open_c)

    @staticmethod
    def __prepare(event: WeatherEvent, code: int) -> (BlindMock, TriggerMock):
        blind = get_blind()
        blind.add_event(event)
        jsn = get_json()
        jsn['weather'][0]['id'] = code
        w = Weather(jsn)
        trigger = TriggerMock(w)
        return blind, trigger


def get_blind(name: str = 'Test') -> BlindMock:
    return BlindMock(name)


def get_json():
    with open('tests/mock/weather.json', 'r') as stream:
        return json.loads(stream.read())


if __name__ == '__main__':
    unittest.main()
