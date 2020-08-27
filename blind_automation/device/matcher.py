#!/usr/bin/env python3
import logging

from .device import Typ
from .shelly import Shelly

logger = logging.getLogger(__name__)


def create(id: str, typ: Typ):
    return Shelly(id)
