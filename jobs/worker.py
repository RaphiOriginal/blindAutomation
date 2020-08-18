#!/usr/bin/env python3
import logging
import time

logger = logging.getLogger(__name__)


def work(task):
    while not task.ready():
        time.sleep(5)
    if not task.done():
        if task.do():
            logger.info('Successfully done {}'.format(task))
