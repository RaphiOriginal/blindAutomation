#!/usr/bin/env python3
from datetime import datetime
from sched import scheduler

from ..building.interface import Shutter
from .worker import batch


class Job:
    def __init__(self, trigger, blind: Shutter):
        self.__trigger = trigger
        self.__blind: Shutter = blind
        self.__applies: bool = trigger.applies()

    def schedule(self, schedule: scheduler):
        """Schedules the Job at the given timestamp"""
        tasks = self.__trigger.task().get(self.__blind)
        schedule.enterabs(self.__trigger.time(), 1, batch, argument=(tasks,))

    def get_time(self) -> datetime:
        return self.__trigger.time()

    def get_id(self) -> str:
        return self.__blind.id

    def applies(self) -> bool:
        return self.__applies

    def __repr__(self):
        return 'Job: { trigger: %s, blind: %s at: %s}' % \
               (self.__trigger.type(), self.__blind.name, self.__trigger.time())
