#!/usr/bin/env python3
import logging
import sched
import time
from collections import defaultdict
from datetime import datetime, timedelta

import global_date
from jobs.interface import PriorityManager
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
        self.__priority_manager = self.PriorityManager()

    def add(self, job: Job):
        self.__jobs[job.get_id()].append(job)
        return self

    def prepare(self):
        """Removes all jobs in the past except for the last one, to ensure at least the last one will be executed!"""
        for shelly, jobs in self.__jobs.items():
            jobs.sort(key=lambda job: job.get_time())

            future = list(filter(lambda job: job.get_time() > datetime.now(global_date.zone), jobs))

            logger.info('{} jobs prepared for {}:'.format(len(future), shelly))
            for job in future:
                job.schedule(self.__schedule, self.__priority_manager)
                logger.info(job)

        self.__jobs = defaultdict(list)
        return self

    def run(self) -> bool:
        if not self.__schedule.empty():
            self.__schedule.run()
        return not self.__schedule.empty()

    class PriorityManager(PriorityManager):
        def __init__(self):
            self.__priority_map = defaultdict(int)

        def prio(self, runtime: datetime) -> int:
            if self.__priority_map[runtime]:
                next = self.__priority_map[runtime]
                self.__priority_map[runtime] = next + 1
                return next
            self.__priority_map[runtime] = 2
            return 1


manager = JobManager()
