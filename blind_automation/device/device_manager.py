#!/usr/bin/env python3
import logging
import time

from zeroconf import ServiceBrowser, Zeroconf

from blind_automation.device.device import Device

logger = logging.getLogger(__name__)


class DeviceHandler:

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


class DeviceManager:
    def __init__(self, devices: [Device]):
        self.__devices: [Device] = devices
        self.__running = False

    def run(self):
        self.__running = True
        zeroconf = Zeroconf()
        handler = DeviceHandler(self.__devices)
        ServiceBrowser(zeroconf, "_http._tcp.local.", handler)
        try:
            while self.__running:
                time.sleep(0.01)
        finally:
            zeroconf.close()

    def stop(self):
        self.__running = False
