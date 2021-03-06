import json
import unittest
from typing import Optional

from blind_automation.building.blind.blind import Blind
from blind_automation.jobs.task import Open, Tilt, Close
from tests.mock.device import DeviceMock
from tests.mock.trigger_mock import TriggerMock
from blind_automation.weather import event
from blind_automation.weather.enum import WeatherConditionEnum, WeatherSubConditionEnum
from blind_automation.weather.event import CloudsEvent, WeatherEvent, RainEvent, ClearEvent, StormEvent, DrizzleEvent, SnowEvent, \
    SpecialWeatherEvent, WindEvent
from blind_automation.weather.weather import Weather


class WeatherEventCase(unittest.TestCase):
    def test_clouds(self):
        # Setup
        e = CloudsEvent()
        b, trigger = self.__prepare([e], 804, percentage=100)
        # Test
        b.update(trigger)
        # Check
        self.assertEqual(1, b.device.open_counter)

    def test_clouds_not_applying(self):
        # Setup
        e = CloudsEvent()
        b, trigger = self.__prepare([e], 804, percentage=94)
        # Test
        b.update(trigger)
        # Check
        self.assertEqual(0, b.device.open_counter)

    def test_rain(self):
        # Setup
        e = RainEvent()
        b, trigger = self.__prepare([e], 504)
        # Test
        b.update(trigger)
        # Check
        self.assertEqual(1, b.device.open_counter)

    def test_rain_not_applying(self):
        # Setup
        e = RainEvent()
        b, trigger = self.__prepare([e], 500)
        # Test
        b.update(trigger)
        # Check
        self.assertEqual(0, b.device.open_counter)

    def test_clear(self):
        # Setup
        e = ClearEvent()
        b, trigger = self.__prepare([e], 800)
        # Test
        b.update(trigger)
        # Check
        self.assertEqual(1, b.device.close_counter)

    def test_clear_not_applying(self):
        # Setup
        e = ClearEvent()
        b, trigger = self.__prepare([e], 801)
        # Test
        b.update(trigger)
        # Check
        self.assertEqual(0, b.device.close_counter)

    def test_storm(self):
        # Setup
        e = StormEvent()
        b, trigger = self.__prepare([e], 200)
        # Test
        b.update(trigger)
        # Check
        self.assertEqual(1, b.device.open_counter)

    def test_storm_not_applying(self):
        # Setup
        e = StormEvent()
        b, trigger = self.__prepare([e], 300)
        # Test
        b.update(trigger)
        # Check
        self.assertEqual(0, b.device.open_counter)

    def test_drizzle(self):
        # Setup
        e = DrizzleEvent()
        b, trigger = self.__prepare([e], 321)
        # Test
        b.update(trigger)
        # Check
        self.assertEqual(1, b.device.open_counter)

    def test_drizzle_not_applying(self):
        # Setup
        e = DrizzleEvent()
        b, trigger = self.__prepare([e], 300)
        # Test
        b.update(trigger)
        # Check
        self.assertEqual(0, b.device.open_counter)

    def test_snow(self):
        # Setup
        e = SnowEvent()
        b, trigger = self.__prepare([e], 611)
        # Test
        b.update(trigger)
        # Check
        self.assertEqual(1, b.device.open_counter)

    def test_snow_not_applying(self):
        # Setup
        e = SnowEvent()
        b, trigger = self.__prepare([e], 300)
        # Test
        b.update(trigger)
        # Check
        self.assertEqual(0, b.device.open_counter)

    def test_atmosphere(self):
        # Setup
        e = SpecialWeatherEvent()
        b, trigger = self.__prepare([e], 701)
        # Test
        b.update(trigger)
        # Check
        self.assertEqual(1, b.device.open_counter)

    def test_atmosphere_not_applying(self):
        # Setup
        e = SpecialWeatherEvent()
        b, trigger = self.__prepare([e], 300)
        # Test
        b.update(trigger)
        # Check
        self.assertEqual(0, b.device.open_counter)

    def test_wind(self):
        #Setup
        e = WindEvent()
        e.set_speed(1)
        b, trigger = self.__prepare([e], 300)
        #Test
        b.update(trigger)
        #Check
        self.assertEqual(1, b.device.open_counter)

    def test_wind_not_applying(self):
        #Setup
        e = WindEvent()
        e.set_speed(2)
        b, trigger = self.__prepare([e], 300)
        #Test
        b.update(trigger)
        #Check
        self.assertEqual(0, b.device.open_counter)

    def test_wind_direction(self):
        #Setup
        e = WindEvent()
        e.set_speed(1)
        e.set_direction(164, 166)
        b, trigger = self.__prepare([e], 300)
        #Test
        b.update(trigger)
        #Check
        self.assertEqual(1, b.device.open_counter)

    def test_wind_direction_not_applying(self):
        #Setup
        e = WindEvent()
        e.set_speed(1)
        e.set_direction(160, 164)
        b, trigger = self.__prepare([e], 300)
        #Test
        b.update(trigger)
        #Check
        self.assertEqual(0, b.device.open_counter)

    def test_wind_speed_not_applying(self):
        #Setup
        e = WindEvent()
        e.set_speed(2)
        e.set_direction(164, 166)
        b, trigger = self.__prepare([e], 300)
        #Test
        b.update(trigger)
        #Check
        self.assertEqual(0, b.device.open_counter)

    def test_wind_inverted_direction(self):
        #Setup
        e = WindEvent()
        e.set_speed(1)
        e.set_direction(166, 90)
        b, trigger = self.__prepare([e], 300)
        #Test
        b.update(trigger)
        #Check
        self.assertEqual(1, b.device.open_counter)

    def test_wind_inverted_direction_not_applying(self):
        #Setup
        e = WindEvent()
        e.set_speed(1)
        e.set_direction(164, 90)
        b, trigger = self.__prepare([e], 300)
        #Test
        b.update(trigger)
        #Check
        self.assertEqual(1, b.device.open_counter)

    def test_night_mode_blocking(self):
        e = ClearEvent()
        b, trigger = self.__prepare([e], 800, 2)
        # Test
        b.update(trigger)
        self.assertEqual(0, b.device.close_counter)

    def test_night_mode_deactivated(self):
        e = ClearEvent()
        e.set_night_mode(False)
        b, trigger = self.__prepare([e], 800, 2)
        # Test
        b.update(trigger)
        self.assertEqual(1, b.device.close_counter)

    @staticmethod
    def __prepare(events: [WeatherEvent], code: int, hours: int = 0, percentage: Optional[int] = None) -> (Blind, TriggerMock):
        b = get_blind()
        b.add_events(events)
        jsn = get_json()
        jsn['weather'][0]['id'] = code
        jsn['dt'] = jsn['dt'] + hours * 3600
        if percentage:
            jsn['clouds']['all'] = percentage
        w = Weather(jsn)
        trigger = TriggerMock(w)
        return b, trigger


class WeatherEventBuilder(unittest.TestCase):
    def test_clouds(self):
        events = ['CLOUDY', {'CLOUDY': {'task': 'TILT', 'coverage': 93}}]
        b = blind(events)
        event.apply_weather_events(b)
        result = b.events
        self.assertEqual(2, len(result))
        self.assertEqual(Open.type(), result[0]._task.type())
        self.assertEqual(Tilt.type(), result[1]._task.type())
        item = result[0]
        self.assertEqual(CloudsEvent.type(), item.type())
        self.assertEqual(WeatherConditionEnum.CLOUDS, item._main)
        self.assertEqual(0, len(item._sub))
        self.assertEqual(100, item.percentage)
        item = result[1]
        self.assertEqual(CloudsEvent.type(), item.type())
        self.assertEqual(WeatherConditionEnum.CLOUDS, item._main)
        self.assertEqual(0, len(item._sub))
        self.assertEqual(93, item.percentage)

    def test_clear(self):
        events = ['CLEAR', {'CLEAR': {'task': 'TILT'}}]
        b = blind(events)
        event.apply_weather_events(b)
        result = b.events
        self.assertEqual(2, len(result))
        for e in result:
            self.assertEqual(WeatherConditionEnum.CLEAR, e._main)
            self.assertEqual('CLEAR', e.type())
        self.assertEqual(Tilt.type(), result[1]._task.type())

    def test_special_weather(self):
        events = ['SPECIAL', {'SPECIAL': {'task': 'TILT', 'events': ['TORNADO']}}]
        b = blind(events)
        event.apply_weather_events(b)
        result = b.events
        self.assertEqual(2, len(result))
        for e in result:
            self.assertEqual(WeatherConditionEnum.ATMOSPHERE, e._main)
            self.assertEqual('SPECIAL', e.type())
        self.assertEqual(1, len(result[1]._sub))
        self.assertEqual(WeatherSubConditionEnum.TORNADO, result[1]._sub[0])
        self.assertEqual(Tilt.type(), result[1]._task.type())

    def test_snow(self):
        events = ['SNOW', {'SNOW': {'task': 'TILT', 'intensity': ['SLEET']}}]
        b = blind(events)
        event.apply_weather_events(b)
        result = b.events
        self.assertEqual(2, len(result))
        for e in result:
            self.assertEqual(WeatherConditionEnum.SNOW, e._main)
            self.assertEqual('SNOW', e.type())
        self.assertEqual(1, len(result[1]._sub))
        self.assertEqual(WeatherSubConditionEnum.SLEET, result[1]._sub[0])
        self.assertEqual(Tilt.type(), result[1]._task.type())

    def test_rain(self):
        events = ['RAIN', {'RAIN': {'task': 'TILT', 'intensity': ['HEAVY']}}]
        b = blind(events)
        event.apply_weather_events(b)
        result = b.events
        self.assertEqual(2, len(result))
        for e in result:
            self.assertEqual(WeatherConditionEnum.RAIN, e._main)
            self.assertEqual('RAIN', e.type())
        self.assertEqual(1, len(result[1]._sub))
        self.assertEqual(WeatherSubConditionEnum.HEAVY, result[1]._sub[0])
        self.assertEqual(Tilt.type(), result[1]._task.type())

    def test_drizzle(self):
        events = ['DRIZZLE', {'DRIZZLE': {'task': 'TILT', 'intensity': ['SHOWER']}}]
        b = blind(events)
        event.apply_weather_events(b)
        result = b.events
        self.assertEqual(2, len(result))
        for e in result:
            self.assertEqual(WeatherConditionEnum.DRIZZLE, e._main)
            self.assertEqual('DRIZZLE', e.type())
        self.assertEqual(1, len(result[1]._sub))
        self.assertEqual(WeatherSubConditionEnum.SHOWER, result[1]._sub[0])
        self.assertEqual(Tilt.type(), result[1]._task.type())

    def test_storm(self):
        events = ['STORM', {'STORM': {'task': 'TILT', 'intensity': ['RAGGED']}}]
        b = blind(events)
        event.apply_weather_events(b)
        result = b.events
        self.assertEqual(2, len(result))
        for e in result:
            self.assertEqual(WeatherConditionEnum.STORM, e._main)
            self.assertEqual('STORM', e.type())
        self.assertEqual(1, len(result[1]._sub))
        self.assertEqual(WeatherSubConditionEnum.RAGGED, result[1]._sub[0])
        self.assertEqual(Tilt.type(), result[1]._task.type())

    def test_wind(self):
        events = ['WIND', {'WIND': {'task': 'TILT', 'speed': 100, 'direction': {'from': 100, 'to': 200}}}]
        b = blind(events)
        event.apply_weather_events(b)
        result = b.events
        self.assertEqual(2, len(result))
        for e in result:
            self.assertEqual('WIND', e.type())
        self.assertEqual(120.0, result[0].speed)
        self.assertEqual(100, result[1].speed)
        self.assertIsNone(result[0].direction[0])
        self.assertIsNone(result[0].direction[1])
        self.assertEqual((100, 200), result[1].direction)
        self.assertEqual(Tilt.type(), result[1]._task.type())

    def test_override_night_mode(self):
        events = [{'CLEAR': {'night': False}}]
        b = blind(events)
        event.apply_weather_events(b)
        result = b.events
        self.assertEqual(1, len(result))
        for e in result:
            self.assertEqual(WeatherConditionEnum.CLEAR, e._main)
            self.assertEqual('CLEAR', e.type())
            self.assertFalse(e._night_mode)

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

    def test_day_extraction(self):
        events = [{'RAIN': {'at': ['WEEKEND']}}]
        b = blind(events)
        event.apply_weather_events(b)
        result = b.events
        self.assertEqual(1, len(result))
        e = result[0]
        self.assertEqual(2, len(e._on))
        for day in e._on:
            self.assertTrue(day in ['SU', 'SA'], 'Day {} not in list {}'.format(day, e._on))

    def test_day_extraction_default(self):
        events = ['RAIN']
        b = blind(events)
        event.apply_weather_events(b)
        result = b.events
        self.assertEqual(1, len(result))
        e = result[0]
        self.assertEqual(7, len(e._on))


class WeatherBlockerTestCase(unittest.TestCase):
    def test_blocking(self):
        # Setup
        e = CloudsEvent()
        b, trigger = self.__prepare([e], 804, percentage=100)
        # Test
        b.update(trigger)
        # Check
        self.assertEqual(1, b.device.open_counter)
        self.assertTrue(b.blocked)
        Close(b).do()
        Open(b).do()
        self.assertEqual(0, b.device.close_counter)
        self.assertEqual(1, b.device.open_counter)
        self.assertEqual(Open.type(), b._blocker.last.type())

    def test_unblocking(self):
        # Setup
        e = CloudsEvent()
        b, trigger = self.__prepare([e], 804, percentage=100)
        # Test
        b.update(trigger)
        # Check
        self.assertEqual(1, b.device.open_counter)
        self.assertTrue(b.blocked)
        Close(b).do()
        Open(b).do()
        self.assertEqual(0, b.device.close_counter)
        self.assertEqual(1, b.device.open_counter)
        self.assertEqual(Open.type(), b._blocker.last.type())
        release = self.__create_trigger(803, percentage=93)
        b.update(release)
        self.assertFalse(b.blocked, 'Blocking should be released')
        self.assertEqual(1, b.device.close_counter, 'Last blocked Task should be applied')
        Close(b).do()
        self.assertEqual(2, b.device.close_counter, 'Further task shouldn\'t be blocked')

    def test_event_order(self):
        # Setup
        c = CloudsEvent()
        r = RainEvent()
        b, trigger = self.__prepare([c, r], 804, percentage=100)
        print(b)
        # Test
        b.update(trigger)
        # Check
        rain_trigger = self.__create_trigger(504, percentage=93)
        b.update(rain_trigger)
        print(b)
        self.assertTrue(b.blocked)
        # Unblocks first event and then blocks with second event
        self.assertEqual(2, b.device.open_counter)
        self.assertFalse(c.active)
        self.assertTrue(r.active)

    def test_event_reverse(self):
        # Setup
        c = CloudsEvent()
        r = RainEvent()
        b, trigger = self.__prepare([r, c], 804, percentage=100)
        print(b)
        # Test
        b.update(trigger)
        print(b)
        self.assertTrue(b.blocked)
        # Check
        rain_trigger = self.__create_trigger(504, percentage=93)
        b.update(rain_trigger)
        self.assertTrue(b.blocked)
        # Unblocks first event and then blocks with second event
        self.assertEqual(2, b.device.open_counter)

    def test_only_one_active_event(self):
        # Setup
        c = CloudsEvent()
        r = RainEvent()
        b, trigger = self.__prepare([r, c], 804, percentage=100)
        print(b)
        # Test
        b.update(trigger)
        print(b)
        self.assertTrue(b.blocked)
        # Check
        rain_trigger = self.__create_trigger(504, percentage=100)
        rain_trigger.trigger.conditions.append(trigger.trigger.conditions[0])
        b.update(rain_trigger)
        self.assertTrue(b.blocked)
        self.assertTrue(c.active, 'Clouds should still be active')
        self.assertFalse(r.active, 'Rain should not get activated')

    @staticmethod
    def __prepare(events: [WeatherEvent], code: int, hours: int = 0, percentage: Optional[int] = None) -> (Blind, TriggerMock):
        b = get_blind()
        b.add_events(events)
        jsn = get_json()
        jsn['weather'][0]['id'] = code
        jsn['dt'] = jsn['dt'] + hours * 3600
        if percentage:
            jsn['clouds']['all'] = percentage
        w = Weather(jsn)
        trigger = TriggerMock(w)
        return b, trigger

    @staticmethod
    def __create_trigger(code: int, percentage: Optional[int] = None) -> TriggerMock:
        jsn = get_json()
        jsn['weather'][0]['id'] = code
        if percentage:
            jsn['clouds']['all'] = percentage
        w = Weather(jsn)
        return TriggerMock(w)


def get_blind(name: str = 'Test') -> Blind:
    return Blind(name, 10, 20, DeviceMock(name), [], [])


def blind(events: []) -> Blind:
    return Blind('test', 10, 20, DeviceMock('YOLO'), [], events)


def get_json():
    with open('tests/mock/weather.json', 'r') as stream:
        return json.loads(stream.read())


if __name__ == '__main__':
    unittest.main()
