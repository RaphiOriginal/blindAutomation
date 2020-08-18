import logging

from device.device import Typ
from shelly.shelly import Shelly

logger = logging.getLogger(__name__)


def create(id: str, typ: Typ):
    return Shelly(id)
