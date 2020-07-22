class Shelly:
    ip: str = None

    def __init__(self, name: str, id: str, direction: str):
        self.name: str = name
        self.id: str = id
        self.direction: str = direction

    def __repr__(self):
        return 'Shelly: { name: %s, id: %s, direction: %s, ip: %s}' % (self.name, self.id, self.direction, self.ip)
