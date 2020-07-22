import requests
import yaml

from shelly.shelly import Shelly


def checkId(shellys, text):
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


def find_shellys(mask):
    potentialPool: [(str, str)] = []
    for end in range(1, 255):
        try:
            ip = mask + str(end)
            url = '{}/shelly/'.format(ip)
            r = requests.get(url, timeout=0.3)
            if r.status_code == 200:
                print('found ' + r.text)
                potentialPool.append((ip, r.text))
        except Exception as e:
            print(e)
    return potentialPool


def update_configured_shellys(shellys, pool):
    for shelly in shellys:
        match = list(filter(lambda entry: shelly.id.upper() in entry[1], pool))
        if len(match) != 1:
            raise ValueError('multiple or none device found in network for configured Shelly {}'.format(shelly.id))
        else:
            shelly.ip = match[0][0]


def collect():
    shellys = prepare_shellys()
    pool = find_shellys('http://192.168.178.')
    update_configured_shellys(shellys, pool)

    return shellys
