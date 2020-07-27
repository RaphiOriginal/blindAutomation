#!/usr/bin/env python3
import logging
import time

import requests

logger = logging.getLogger(__name__)


def work(task):
    while not task.ready():
        time.sleep(5)
    if not task.done():
        order = requests.get(task.do())
        if order.status_code != 200:
            logger.error('Call with {} failed with status {} and content: {}'.format(task.do(), order.status_code, order.text))
        else:
            logger.info('Task {} completed: {}'.format(task.do(), order.text))
