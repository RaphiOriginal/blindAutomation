import logging
import time

from zeroconf import ServiceBrowser, Zeroconf

from device.device import Device

logger = logging.getLogger(__name__)


class DeviceListener:

    def __init__(self, devices):
        self.devices: [Device] = devices

    def remove_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        logger.debug("Service %s removed, service info: %s" % (name, info))
        for device in self.devices:
            if device.id.upper() in name:
                device.deactivate()

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        logger.debug("Service %s added, service info: %s" % (name, info))
        for device in self.devices:
            if device.id.upper() in name:
                device.url = 'http://' + '.'.join(str(c) for c in info.addresses[0])
                device.activate()

    def update_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        logger.debug("Service %s updated, service info: %s" % (name, info))
        for device in self.devices:
            if device.id.upper() in name:
                device.url = 'http://' + '.'.join(str(c) for c in info.addresses[0])
                device.activate()



def find_devices(devices):
    logger.setLevel(logging.INFO)
    zeroconf = Zeroconf()
    listener = DeviceListener(devices)
    try:
        while True:
            ServiceBrowser(zeroconf, "_http._tcp.local.", listener)
            time.sleep(3)
    finally:
        zeroconf.close()
