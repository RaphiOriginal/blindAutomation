#!/usr/bin/env python3
import logging
import sched
import time
from collections import defaultdict
from datetime import datetime, timedelta

import global_date
from jobs.job import Job

logger = logging.getLogger(__name__)


def now():
    return datetime.now(global_date.zone)


def delay(delta):
    if isinstance(delta, timedelta):
        until = datetime.now(global_date.zone) + delta
        logger.info('Wait until {}'.format(until.isoformat()))
        time.sleep(delta.total_seconds())
    if isinstance(delta, int):
        time.sleep(delta)


class JobManager:
    def __init__(self):
        self.__schedule = sched.scheduler(now, delay)
        self.__jobs = defaultdict(list)

    def add(self, job: Job):
        self.__jobs[job.get_id()].append(job)
        return self

    def prepare(self):
        """
        Removes all jobs in the past, to ensure at least the last one will be executed!
        It also removes all jobs which do not fulfill the condition to be applied e.g. wrong weekday
        """
        for shelly, jobs in self.__jobs.items():
            jobs.sort(key=lambda job: job.get_time())

            applies = list(filter(lambda job: job.applies(), jobs))
            future = list(filter(lambda job: job.get_time() > datetime.now(global_date.zone), applies))

            logger.info('{} jobs prepared for {}:'.format(len(future), shelly))
            for job in future:
                job.schedule(self.__schedule)
                logger.info(job)

        return self

    def run(self) -> bool:
        if not self.__schedule.empty():
            self.__schedule.run()
            self.__jobs = defaultdict(list)
        return not self.__schedule.empty()

    @property
    def jobs(self) -> [Job]:
        return self.__jobs

    def __repr__(self):
        return 'JobManager: { length: %s, queue: %s }' % (len(self.__schedule.queue), self.__schedule.queue)


manager = JobManager()
