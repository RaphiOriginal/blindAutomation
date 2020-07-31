#!/usr/bin/env python3
import asyncio
import logging
from collections import defaultdict
from concurrent.futures.thread import ThreadPoolExecutor
from ipaddress import IPv4Network

import requests
import yaml

from blinds.blind import Blind
from settings.settings import NetworkSettings
from shelly.shelly import Shelly
from blinds.wall import Wall

scheme = 'http://'
config = 'settings.yaml'

logger = logging.getLogger(__name__)


def check_id(shellys, text):
    for shelly in shellys:
        if shelly.id.upper() in text:
            return True
    return False


def prepare_walls() -> [Wall]:
    walls: [Wall] = []
    with open(config, 'r') as stream:
        data = yaml.safe_load(stream)
        for wall in data.get('walls'):
            w = Wall(wall.get('name'), wall.get('in'), wall.get('out'))
            triggers: [] = []
            if 'blinds' in wall:
                for blind in wall.get('blinds'):
                    in_sun = w.in_sun
                    out_sun = w.out_sun
                    s = blind.get('shelly')
                    shelly = Shelly(s.get('name'), str(s.get('id')))
                    if 'triggers' in blind.keys():
                        triggers = blind.get('triggers')
                    if 'in' in blind.keys():
                        in_sun = blind.get('in')
                    if 'out' in blind.keys():
                        out_sun = blind.get('out')
                    w.add_blind(Blind(in_sun, out_sun, shelly, triggers))
                walls.append(w)

    return walls


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
                    logger.info('response: {}'.format(response))
                    shellys.append(response)
    return shellys


def collect():
    settings = NetworkSettings(config)
    mask = IPv4Network(settings.mask)
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(collect_shellys(mask))
    pool = loop.run_until_complete(future)

    walls = prepare_walls()

    walls = update_configured_shellys(walls, pool)
    return walls


def update_configured_shellys(walls: [Wall], pool) -> [Wall]:
    updated: [Wall] = []
    for wall in walls:
        updated_blinds: [Blind] = []
        for blind in wall.blinds:
            shelly = blind.shelly
            match = list(filter(lambda entry: shelly.id.upper() in entry[1].get('mac'), pool))
            if len(match) != 1:
                logger.info('{} devices found in network for configured Shelly: {}'.format(len(match), shelly))
            else:
                if len(match[0]) <= 1 or match[0][1].get('rollers') is None or \
                        not match[0][1].get('rollers')[0].get('positioning') or match[0][0] is None:
                    logger.error('Shelly {} not configured as roller or calibrated'.format(shelly))
                    continue

                shelly.url = match[0][0]
                updated_blinds.append(blind)
        wall.blinds = updated_blinds
        if len(wall.blinds) > 0:
            updated.append(wall)
    logger.info('Updated Walls: {}'.format(updated))
    return updated
