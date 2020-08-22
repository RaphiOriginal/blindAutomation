import json
import unittest

from building.blind import Blind
from jobs.task import Open, Tilt
from tests.mock.blind_mock import BlindMock
from tests.mock.trigger_mock import TriggerMock
from weather import event
from weather.enum import WeatherConditionEnum, WeatherSubConditionEnum
from weather.event import CloudsEvent, WeatherEvent
from weather.weather import Weather


class WeatherEventCase(unittest.TestCase):
    def test_clouds(self):
        # Setup
        e = CloudsEvent()
        b, trigger = self.__prepare([e], 804)
        # Test
        b.update(trigger)
        # Check
        self.assertEqual(1, b.open_c)

    @staticmethod
    def __prepare(events: [WeatherEvent], code: int) -> (BlindMock, TriggerMock):
        b = get_blind()
        b.add_events(events)
        jsn = get_json()
        jsn['weather'][0]['id'] = code
        w = Weather(jsn)
        trigger = TriggerMock(w)
        return b, trigger


class WeatherEventBuilder(unittest.TestCase):
    def test_clouds(self):
        events = ['CLOUDY', {'CLOUDY': {'task': 'TILT', 'intensity': ['SCATTERED']}}]
        b = blind(events)
        event.apply_weather_events(b)
        result = b._events
        self.assertEqual(2, len(result))
        self.assertEqual(Open.type(), result[0]._task.type())
        self.assertEqual(Tilt.type(), result[1]._task.type())
        item = result[0]
        self.assertEqual(CloudsEvent.type(), item.type())
        self.assertEqual(WeatherConditionEnum.CLOUDS, item._main)
        self.assertEqual(1, len(item._sub))
        self.assertEqual(WeatherSubConditionEnum.OVERCAST, item._sub[0])
        item = result[1]
        self.assertEqual(CloudsEvent.type(), item.type())
        self.assertEqual(WeatherConditionEnum.CLOUDS, item._main)
        self.assertEqual(1, len(item._sub))
        self.assertEqual(WeatherSubConditionEnum.SCATTERED, item._sub[0])

    def test_multi_sub(self):
        events = [{'CLOUDY': {'intensity': ['SCATTERED', 'OVERCAST']}}]
        b = blind(events)
        event.apply_weather_events(b)
        result = b._events[0]
        self.assertEqual(1, len(b._events))
        self.assertEqual(Open.type(), result._task.type())
        self.assertEqual(CloudsEvent.type(), result.type())
        self.assertEqual(WeatherConditionEnum.CLOUDS, result._main)
        self.assertEqual(2, len(result._sub))
        self.assertEqual(WeatherSubConditionEnum.SCATTERED, result._sub[0])
        self.assertEqual(WeatherSubConditionEnum.OVERCAST, result._sub[1])


def get_blind(name: str = 'Test') -> BlindMock:
    return BlindMock(name)


def blind(events: []) -> Blind:
    return Blind('test', 10, 20, None, [], events)


def get_json():
    with open('tests/mock/weather.json', 'r') as stream:
        return json.loads(stream.read())


if __name__ == '__main__':
    unittest.main()
