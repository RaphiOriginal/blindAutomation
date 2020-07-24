#!/usr/bin/env python3
import time

import requests


def work(task):
    while not task.ready():
        time.sleep(5)
    if not task.done():
        order = requests.get(task.do())
        if order.status_code != 200:
            print('Call with {} failed with status {} and content {}'.format(task.do(), order.status_code, order.text))
        else:
            print('Task {} completed: {}'.format(task.do(), order.text))