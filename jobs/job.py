#!/usr/bin/env python3
from datetime import datetime, tzinfo
from sched import scheduler

from jobs.task import Open, Close, Tilt, PreTilt, Task
from jobs.worker import work
from shelly.shelly import Shelly


class Job:
    def __init__(self, time: datetime, shelly: Shelly, task: Task):
        self.__time: datetime = time
        self.tzinfo: tzinfo = time.tzinfo
        self.__shelly: Shelly = shelly
        self.__task: Task = task

    def schedule(self, schedule: scheduler):
        """Schedules the Job at the given timestamp"""
        tasks = self.__task.get_for(self.__shelly)
        prio = 1
        for task in tasks:
            schedule.enterabs(self.__time, prio, work, argument=task)
            prio += 1

    def get_time(self) -> datetime:
        return self.__time

    def get_id(self):
        return self.__shelly.id

    def __repr__(self):
        return 'Job: { time: %s, shelly: %s, task: %s' % (self.__time, self.__shelly, self.__task)