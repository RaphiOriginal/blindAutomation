#!/usr/bin/env python3
import asyncio
import logging
from concurrent.futures.thread import ThreadPoolExecutor
from ipaddress import IPv4Network

import requests

from settings.settings import NetworkSettings
from shelly.shelly import Shelly

scheme = 'http://'

logger = logging.getLogger(__name__)


def check_id(shellys, text):
    for shelly in shellys:
        if shelly.id.upper() in text:
            return True
    return False


def fetch_shelly(session: requests.Session, base_url: str):
    try:
        url = '{}/status'.format(base_url)
        r = session.get(url, timeout=3)
        logger.debug(r)
        if r.status_code == 200 and r.json() is not None:
            logger.info('🎉 found on {} with: {}'.format(base_url, r.text))
            return base_url, r.json()
    except Exception as e:
        logger.debug('{}: no shelly found error: {}'.format(base_url, e))


async def collect_shellys(mask: IPv4Network):
    shellys: [Shelly] = []
    with ThreadPoolExecutor(max_workers=253) as executor:
        with requests.Session() as session:
            loop = asyncio.get_event_loop()
            potentials = [
                loop.run_in_executor(
                    executor, fetch_shelly, *(session, '{}{}'.format(scheme, ip.exploded))
                )
                for ip in mask.hosts()
            ]
            for response in await asyncio.gather(*potentials):
                if response is not None:
                    logger.info('response: {}'.format(response))
                    shellys.append(response)
    return shellys


def collect_devices():
    settings = NetworkSettings()
    mask = IPv4Network(settings.mask)
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(collect_shellys(mask))
    pool = loop.run_until_complete(future)
    return pool

