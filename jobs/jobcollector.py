import sched
import time
from collections import defaultdict
from datetime import datetime, timedelta

from dateutil import tz

from jobs.job import Job


class Jobcollector:
    def __init__(self):
        self.__schedule = sched.scheduler(self.__now, self.__delay)
        self.__jobs = defaultdict(list)

    def add(self, job: Job):
        self.__jobs[job.get_id()].append(job)
        return self

    def collect(self):
        """Removes all jobs in the past except for the last one, to ensure at least the last one will be executed!"""
        for shelly, jobs in self.__jobs.items():
            jobs.sort(key=lambda job: job.get_time())

            future = list(filter(lambda job: job.get_time() > datetime.now(job.tzinfo), jobs))
            past = list(filter(lambda job: job.get_time() < datetime.now(job.tzinfo), jobs))
            if len(past) > 0:
                last = past[len(past) - 1]
                last.schedule(self.__schedule)
                print('One past job collected for {}: {}'.format(shelly, last))

            for job in future:
                job.schedule(self.__schedule)
            print('{} jobs collected for {}: {}'.format(len(future), shelly, future))

        return self

    def run(self):
        self.__schedule.run()

    def __now(self):
        return datetime.now(tz.tzlocal())

    def __delay(self, delta):
        if isinstance(delta, timedelta):
            time.sleep(delta.seconds)
        if isinstance(delta, int):
            time.sleep(delta)
