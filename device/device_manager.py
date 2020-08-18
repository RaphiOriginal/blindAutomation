import logging
import time

from zeroconf import ServiceBrowser, Zeroconf

from device.device import Device

logger = logging.getLogger(__name__)


class DeviceListener:

    def __init__(self, devices):
        self.devices: [Device] = devices

    @staticmethod
    def remove_service(zeroconf, type, name):
        logger.debug("Service %s removed" % (name,))

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        logger.debug("Service %s added, service info: %s" % (name, info))
        for device in self.devices:
            if device.id.upper() in name:
                device.url = 'http://' + '.'.join(str(c) for c in info.addresses[0])
                device.activate()


def find_devices(devices):
    zeroconf = Zeroconf()
    listener = DeviceListener(devices)
    ServiceBrowser(zeroconf, "_http._tcp.local.", listener)
    time.sleep(3)
    zeroconf.close()
