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
        self.__last_job = defaultdict(int)

    def add(self, job: Job):
        self.__jobs[job.get_id()].append(job)
        self.__last_job[job.get_id()] += 1
        return self

    def collect(self):
        """Removes all jobs in the past except for the last one, to ensure at least the last one will be executed!"""
        for shelly, jobs in self.__jobs.items():
            jobs.sort(key=lambda job: job.get_time())

            future = list(filter(lambda job: job.get_time() > datetime.now(job.tzinfo), jobs))
            if len(future) == 0:
                last = jobs[self.__last_job[shelly] - 1]
                last.schedule(self.__schedule)
                print('One job collected for {}: {}'.format(shelly, last))
            else:
                for job in future:
                    job.schedule(self.__schedule)
                print('{} jobs collected for {}: {}'.format(shelly, len(future), future))

        return self

    def run(self):
        self.__schedule.run()

    def __now(self):
        return datetime.now(tz.tzlocal())

    def __delay(self, delta: timedelta):
        time.sleep(delta.seconds)