#!/usr/bin/env python3
class Shelly:
    url: str = None

    def __init__(self, name: str, id: str, direction: str, triggers: []):
        self.name: str = name
        self.id: str = id
        self.direction: str = direction
        self.triggers: [] = triggers

    def get_status(self):
        self.__check_url()
        return '{}/status'.format(self.url)

    def get_roller(self):
        self.__check_url()
        return '{}/roller/0'.format(self.url)

    def set_roller(self, pos):
        self.__check_url()
        return '{}/roller/0?go=to_pos&roller_pos={}'.format(self.url, pos)

    def __check_url(self):
        if self.url is None:
            raise ValueError("URL must be set!")

    def __repr__(self):
        return 'Shelly: { name: %s, id: %s, direction: %s, ip: %s}' % (self.name, self.id, self.direction, self.url)
