#!/usr/bin/env python3
from device.device import Device


class Shelly(Device):

    def __init__(self, id: str):
        self.__id: str = id

    @property
    def id(self):
        return self.__id

    def get_status(self):
        self.__check_url()
        return '{}/status'.format(self.url)

    def stats(self):
        self.__check_url()
        return '{}/roller/0'.format(self.url)

    def move(self, pos):
        self.__check_url()
        return '{}/roller/0?go=to_pos&roller_pos={}'.format(self.url, pos)

    def open(self):
        self.__check_url()
        return '{}/roller/0?go=open'.format(self.url)

    def close(self):
        self.__check_url()
        return '{}/roller/0?go=close'.format(self.url)

    def match(self, pool):
        return list(filter(lambda entry: self.id.upper() in entry[1].get('mac'), pool))

    def validate(self, match) -> bool:
        return len(match) <= 1 or match[1].get('rollers') is None or \
                        not match[1].get('rollers')[0].get('positioning') or match[0] is None

    def __check_url(self):
        if self.url is None:
            raise ValueError("URL must be set!")

    def __repr__(self):
        return 'Shelly: { id: %s, ip: %s}' % (self.__id, self.url)
