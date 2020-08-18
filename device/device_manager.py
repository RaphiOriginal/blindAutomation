import logging
import time

from zeroconf import ServiceBrowser, Zeroconf

from building.blind import Blind

logger = logging.getLogger(__name__)


class DeviceListener:

    def __init__(self, blinds):
        self.blinds: [Blind] = blinds

    @staticmethod
    def remove_service(zeroconf, type, name):
        logger.debug("Service %s removed" % (name,))

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        logger.debug("Service %s added, service info: %s" % (name, info))
        for blind in self.blinds:
            if blind.id.upper() in name:
                blind.device.url = 'http://' + '.'.join(str(c) for c in info.addresses[0])
                blind.activate()


def find_devices(blinds):
    zeroconf = Zeroconf()
    listener = DeviceListener(blinds)
    ServiceBrowser(zeroconf, "_http._tcp.local.", listener)
    time.sleep(3)
    zeroconf.close()
