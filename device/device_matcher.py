import logging

from device.device import Typ
from shelly.shelly import Shelly

logger = logging.getLogger(__name__)


def create(id: str, typ: Typ):
    logger.debug('matching device {} as device typ {}'.format(id, typ))
    return Shelly(id)
