#!/usr/bin/env python3


class Shelly:
    url: str = None

    def __init__(self, id: str):
        self.__id: str = id

    @property
    def id(self):
        return self.__id

    def get_status(self):
        self.__check_url()
        return '{}/status'.format(self.url)

    def get_roller(self):
        self.__check_url()
        return '{}/roller/0'.format(self.url)

    def set_roller(self, pos):
        self.__check_url()
        return '{}/roller/0?go=to_pos&roller_pos={}'.format(self.url, pos)

    def open(self):
        self.__check_url()
        return '{}/roller/0?go=open'.format(self.url)

    def close(self):
        self.__check_url()
        return '{}/roller/0?go=close'.format(self.url)

    def __check_url(self):
        if self.url is None:
            raise ValueError("URL must be set!")

    def __repr__(self):
        return 'Shelly: { id: %s, ip: %s}' % (self.__id, self.url)
