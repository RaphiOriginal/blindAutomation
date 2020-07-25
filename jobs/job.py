#!/usr/bin/env python3
from datetime import datetime, tzinfo
from sched import scheduler

from jobs.worker import work
from shelly.shelly import Shelly


class Job:
    def __init__(self, trigger, shelly: Shelly):
        self.__trigger = trigger
        self.__shelly: Shelly = shelly

    def schedule(self, schedule: scheduler):
        """Schedules the Job at the given timestamp"""
        tasks = self.__trigger.task().get_for(self.__shelly)
        prio = 1
        for task in tasks:
            schedule.enterabs(self.__trigger.time(), prio, work, argument=task)
            prio += 1

    def get_time(self):
        return self.__trigger.time()

    def get_id(self):
        return self.__shelly.id

    def __repr__(self):
        return 'Job: { trigger: %s, shelly: %s }' % (self.__trigger, self.__shelly)
