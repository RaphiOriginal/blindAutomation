
from meteomatics.field import Field
from meteomatics.interval import Interval
from meteomatics.type import Type
from settings.coordinates import Coordinates


class MeteomaticsURLBuilder:

    def __init__(self, base):
        self.__base: str = base
        self.__time: str = 'now'
        self.__timerange: bool = False
        self.__interval: Interval = Interval.HOURLY
        self.__fields: [Field] = []
        self.__location: Coordinates = None
        self.__type: Type = Type.JSON

    def set_time(self, time):
        """setting a specific time in url, if nothing set now is the default"""
        self.__time = time
        self.__timerange = False
        return self

    def set_time_range(self, start, end):
        """setting a rang of time in url, if nothing set only now will be used"""
        self.__time = '{}--{}'.format(start.isoformat(), end.isoformat())
        self.__timerange = True
        return self

    def set_interval(self, interval: Interval):
        """Interval defines the time between each result for time ranges. Hourly is default if nothing is set"""
        self.__interval = interval
        return self

    def add_field(self, field: Field):
        """defines which data should be fetched"""
        self.__fields.append(field.value)
        return self

    def set_location(self, location: Coordinates):
        self.__location = location
        return self

    def set_type(self, type: Type):
        self.__type = type
        return self

    def build(self):
        time = self.__build_time()
        field =  self.__build_fields()
        location = self.__build_location()
        return '{}/{}/{}/{}/{}'.format(self.__base, time, field, location, self.__type.value)

    def __build_time(self):
        time = self.__time
        if self.__timerange:
            time += self.__interval.value

        return time

    def __build_fields(self):
        if len(self.__fields) == 0:
            raise ValueError('At least one field to be set is mandatory')
        return ','.join(self.__fields)

    def __build_location(self):
        if self.__location is None:
            raise ValueError('Location is mandatory')
        return '{},{}'.format(self.__location.lat, self.__location.long)
