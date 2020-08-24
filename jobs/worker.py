#!/usr/bin/env python3
import logging
import time

from jobs.task import Task

logger = logging.getLogger(__name__)


def work(task: Task):
    while not task.ready():
        time.sleep(5)
    if not task.done():
        if task.do():
            logger.info('Successfully done {}'.format(task))
    else:
        logger.info('Task {} already done'.format(task))


def batch(tasks: [Task]):
    for task in tasks:
        work(task)
