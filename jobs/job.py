#!/usr/bin/env python3
from sched import scheduler

from building.blind_interface import BlindInterface
from jobs.worker import work


class Job:
    def __init__(self, trigger, blind: BlindInterface):
        self.__trigger = trigger
        self.__blind: BlindInterface = blind

    def schedule(self, schedule: scheduler):
        """Schedules the Job at the given timestamp"""
        tasks = self.__trigger.task().get(self.__blind)
        prio = 1
        for task in tasks:
            schedule.enterabs(self.__trigger.time(), prio, work, argument=task)
            prio += 1

    def get_time(self):
        return self.__trigger.time()

    def get_id(self):
        return self.__blind.id

    def __repr__(self):
        return 'Job: { trigger: %s, blind: %s }' % (self.__trigger, self.__blind)
