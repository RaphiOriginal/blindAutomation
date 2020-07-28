#!/usr/bin/env python3
import asyncio
import logging
from collections import defaultdict
from concurrent.futures.thread import ThreadPoolExecutor
from ipaddress import IPv4Network

import requests
import yaml

from settings.settings import NetworkSettings
from shelly.shelly import Shelly
from shelly.wall import Wall

scheme = 'http://'
config = 'settings.yaml'

logger = logging.getLogger(__name__)


def check_id(shellys, text):
    for shelly in shellys:
        if shelly.id.upper() in text:
            return True
    return False


def prepare_shellys():
    shellys: [Shelly] = []
    walls = defaultdict(Wall)
    with open(config, 'r') as stream:
        data = yaml.safe_load(stream)
        for wall in data.get('walls'):
            w = wall.get('wall')
            walls[w.get('name')] = Wall(w.get('name'), w.get('in'), w.get('out'))
        for shelly in data.get('shellys'):
            s = shelly.get('shelly')
            triggers: [] = []
            if 'triggers' in s.keys():
                triggers = s.get('triggers')
            w = s.get('wall')
            shellys.append(Shelly(s.get('name'), str(s.get('id')), walls[w], triggers))
    return shellys


def fetch_shelly(session: requests.Session, base_url: str):
    try:
        url = '{}/status/'.format(base_url)
        r = session.get(url, timeout=1)
        if r.status_code == 200:
            logger.info('found on {} with: {}'.format(base_url, r.text))
            return base_url, r.json()
    except Exception as e:
        logger.info(e)


async def collect_shellys(mask: IPv4Network):
    shellys: [Shelly] = []
    with ThreadPoolExecutor(max_workers=100) as executor:
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
                    shellys.append(response)
    return shellys


def collect():
    settings = NetworkSettings(config)
    mask = IPv4Network(settings.mask)
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(collect_shellys(mask))
    pool = loop.run_until_complete(future)

    shellys = prepare_shellys()
    update_configured_shellys(shellys, pool)
    return shellys


def update_configured_shellys(shellys, pool):
    for shelly in shellys:
        match = list(filter(lambda entry: shelly.id.upper() in entry[1].get('mac'), pool))
        if len(match) != 1:
            logger.info('multiple or none device found in network for configured Shelly: {}'.format(shelly))
            shellys.remove(shelly)
        else:
            if len(match[0]) <= 1 or match[0][1].get('rollers') is None or \
                    not match[0][1].get('rollers')[0].get('positioning') or match[0][0] is None:
                logger.error('Shelly {} not configured as roller or calibrated'.format(shelly))
                shellys.remove(shelly)
                pass

            shelly.url = match[0][0]
