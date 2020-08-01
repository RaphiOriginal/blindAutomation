from blinds.blind_state import State
from shelly.shelly import Shelly


class Blind:
    def __init__(self, name: str, sun_in: float, sun_out: float, shelly: Shelly, triggers: []):
        self.name: str = name
        self.sun_in: float = sun_in
        self.sun_out: float = sun_out
        self.shelly: Shelly = shelly
        self.triggers: [] = triggers
        self.state: State = State.UNKNOWN

    def __repr__(self):
        return 'Blind: { name: %s, sun_in: %s, sun_out: %s, shelly: %s, triggers: %s, state: %s }' % \
               (self.name, self.sun_in, self.sun_out, self.shelly, self.triggers, self.state)
