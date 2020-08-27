#!/usr/bin/env python3
import logging

from blind_automation.device.device import Typ
from blind_automation.device.shelly import Shelly

logger = logging.getLogger(__name__)


def create(id: str, typ: Typ):
    return Shelly(id)
