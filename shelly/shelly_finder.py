import asyncio
from concurrent.futures.thread import ThreadPoolExecutor
from ipaddress import IPv4Network

import requests
import yaml

from shelly.shelly import Shelly


prefix = 'http://'


def check_id(shellys, text):
    for shelly in shellys:
        if shelly.id.upper() in text:
            return True
    return False


def prepare_shellys():
    shellys: [Shelly] = []
    with open('shelly/configuration/shelly.yaml', 'r') as stream:
        data = yaml.safe_load(stream)
        for shelly in data.get('shellys'):
            data = shelly.get('shelly')
            shellys.append(Shelly(data.get('name'), str(data.get('id')), data.get('direction')))
    return shellys


def fetch_shelly(session, ip):
    try:
        url = '{}/shelly/'.format(ip)
        r = session.get(url, timeout=1)
        if r.status_code == 200:
            print('found ' + r.text)
            return ip, r.text
    except Exception as e:
        print(e)


async def collect_shellys(mask: IPv4Network):
    shellys: [Shelly] = []
    with ThreadPoolExecutor(max_workers=253) as executor:
        with requests.Session() as session:
            loop = asyncio.get_event_loop()
            potentials = [
                loop.run_in_executor(
                    executor, fetch_shelly, *(session, '{}{}'.format(prefix, ip.exploded))
                )
                for ip in mask.hosts()
            ]
            for response in await asyncio.gather(*potentials):
                if response is not None:
                    shellys.append(response)
    return shellys


def collect():
    mask = IPv4Network('192.168.178.0/24')
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(collect_shellys(mask))
    pool = loop.run_until_complete(future)

    shellys = prepare_shellys()
    update_configured_shellys(shellys, pool)
    return shellys


def update_configured_shellys(shellys, pool):
    for shelly in shellys:
        match = list(filter(lambda entry: shelly.id.upper() in entry[1], pool))
        if len(match) != 1:
            raise ValueError('multiple or none device found in network for configured Shelly {}'.format(shelly.id))
        else:
            shelly.ip = match[0][0]
