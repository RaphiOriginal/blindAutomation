import json
import unittest

from building.blind import Blind
from jobs.task import Open, Tilt, Close
from tests.mock.blind_mock import BlindMock
from tests.mock.trigger_mock import TriggerMock
from weather import event
from weather.enum import WeatherConditionEnum, WeatherSubConditionEnum
from weather.event import CloudsEvent, WeatherEvent, RainEvent
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

    def test_clouds_not_applying(self):
        # Setup
        e = CloudsEvent()
        b, trigger = self.__prepare([e], 803)
        # Test
        b.update(trigger)
        # Check
        self.assertEqual(0, b.open_c)

    def test_rain(self):
        # Setup
        e = RainEvent()
        b, trigger = self.__prepare([e], 504)
        # Test
        b.update(trigger)
        # Check
        self.assertEqual(1, b.open_c)

    def test_rain_not_applying(self):
        # Setup
        e = RainEvent()
        b, trigger = self.__prepare([e], 501)
        # Test
        b.update(trigger)
        # Check
        self.assertEqual(0, b.open_c)

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
        result = b.events
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
        result = b.events[0]
        self.assertEqual(1, len(b._events))
        self.assertEqual(Open.type(), result._task.type())
        self.assertEqual(CloudsEvent.type(), result.type())
        self.assertEqual(WeatherConditionEnum.CLOUDS, result._main)
        self.assertEqual(2, len(result._sub))
        self.assertEqual(WeatherSubConditionEnum.SCATTERED, result._sub[0])
        self.assertEqual(WeatherSubConditionEnum.OVERCAST, result._sub[1])


class WeatherBlockerTestCase(unittest.TestCase):
    def test_blocking(self):
        # Setup
        e = CloudsEvent()
        b, trigger = self.__prepare([e], 804)
        # Test
        b.update(trigger)
        # Check
        self.assertEqual(1, b.open_c)
        self.assertTrue(b.blocker.blocking)
        Close(b).do()
        Open(b).do()
        self.assertEqual(0, b.close_c)
        self.assertEqual(1, b.open_c)
        self.assertEqual(Open.type(), b.blocker.last.type())

    def test_unblocking(self):
        # Setup
        e = CloudsEvent()
        b, trigger = self.__prepare([e], 804)
        # Test
        b.update(trigger)
        # Check
        self.assertEqual(1, b.open_c)
        self.assertTrue(b.blocker.blocking)
        Close(b).do()
        Open(b).do()
        self.assertEqual(0, b.close_c)
        self.assertEqual(1, b.open_c)
        self.assertEqual(Open.type(), b.blocker.last.type())
        release = self.__create_trigger(803)
        b.update(release)
        self.assertFalse(b.blocker.blocking, 'Blocking should be released')
        self.assertEqual(1, b.close_c, 'Last blocked Task should be applied')
        Close(b).do()
        self.assertEqual(2, b.close_c, 'Further task shouldn\'t be blocked')

    def test_event_order(self):
        # Setup
        c = CloudsEvent()
        r = RainEvent()
        b, trigger = self.__prepare([c, r], 804)
        print(b)
        # Test
        b.update(trigger)
        # Check
        rain_trigger = self.__create_trigger(504)
        b.update(rain_trigger)
        self.assertTrue(b.blocker.blocking)
        # Unblocks first event and then blocks with second event
        self.assertEqual(2, b.open_c)

    def test_event_reverse(self):
        # Setup
        c = CloudsEvent()
        r = RainEvent()
        b, trigger = self.__prepare([r, c], 804)
        print(b)
        # Test
        b.update(trigger)
        # Check
        rain_trigger = self.__create_trigger(504)
        b.update(rain_trigger)
        self.assertTrue(b.blocker.blocking)
        # Unblocks first event and then blocks with second event
        self.assertEqual(2, b.open_c)

    def __prepare(self, events: [WeatherEvent], code: int) -> (BlindMock, TriggerMock):
        b = get_blind()
        b.add_events(events)
        trigger = self.__create_trigger(code)
        return b, trigger

    @staticmethod
    def __create_trigger(code: int) -> TriggerMock:
        jsn = get_json()
        jsn['weather'][0]['id'] = code
        w = Weather(jsn)
        return TriggerMock(w)


def get_blind(name: str = 'Test') -> BlindMock:
    return BlindMock(name)


def blind(events: []) -> Blind:
    return Blind('test', 10, 20, None, [], events)


def get_json():
    with open('tests/mock/weather.json', 'r') as stream:
        return json.loads(stream.read())


if __name__ == '__main__':
    unittest.main()
