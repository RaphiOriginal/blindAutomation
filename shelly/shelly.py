class Shelly:
    ip: str = None

    def __init__(self, name: str, id: str, direction: str):
        self.name: str = name
        self.id: str = id
        self.direction: str = direction

    def get_status(self):
        self.__check_ip()
        return '{}/status'.format(self.ip)

    def get_roller(self):
        self.__check_ip()
        return '{}/roller/0'.format(self.ip)

    def set_roller(self, pos):
        self.__check_ip()
        return '{}/roller/0?go=to_pos&roller_pos={}'.format(self.ip, pos)

    def __check_ip(self):
        if self.ip is None:
            raise ValueError("IP must be set!")

    def __repr__(self):
        return 'Shelly: { name: %s, id: %s, direction: %s, ip: %s}' % (self.name, self.id, self.direction, self.ip)
