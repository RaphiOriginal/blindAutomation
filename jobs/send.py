#!/usr/bin/env python3
import time

import requests


def send(url, precondition=None, checkUrl=''):
    if precondition is not None and len(checkUrl) > 0:
        response = requests.get(checkUrl)
        while not condition_met(response, precondition):
            time.sleep(5)
            response = requests.get(checkUrl)

    order = requests.get(url)
    if order.status_code != 200:
        print('Call with {} failed with status {} and content {}'.format(url, order.status_code, order.text))
    else:
        print('Task {} completed: {}'.format(url, order.text))


def condition_met(response, condition):
    data = response.json()
    return data.get('current_pos') == condition
