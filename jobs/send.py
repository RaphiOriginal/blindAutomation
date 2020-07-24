#!/usr/bin/env python3
import time

import requests

from blinds.blind_state import BlindState
from shelly.shelly import Shelly


def send(url, precondition=None, shelly=None):
    if precondition is not None and shelly is not None:
        state = update_state(shelly)
        while not precondition != state.state():
            time.sleep(5)
            update_state()

    order = requests.get(url)
    if order.status_code != 200:
        print('Call with {} failed with status {} and content {}'.format(url, order.status_code, order.text))
    else:
        print('Task {} completed: {}'.format(url, order.text))


def update_state(shelly: Shelly):
    response = requests.get(shelly.get_roller())
    if response.status_code == 200:
        data = response.json()
        return BlindState(data.get('current_pos'), data.get('last_direction'))
    raise ConnectionError('Negative answer from shelly {}: {} - {}'
                          .format(shelly.id, response.status_code, response.text))
