#!/usr/bin/env python3
from datetime import datetime, tzinfo
from sched import scheduler

from blinds.blind_state import State
from jobs.send import send
from jobs.task import Task
from shelly.shelly import Shelly


class Job:
    def __init__(self, time: datetime, shelly: Shelly, task: Task):
        self.__time: datetime = time
        self.tzinfo: tzinfo = time.tzinfo
        self.__shelly: Shelly = shelly
        self.__task: Task = task

    def schedule(self, schedule: scheduler):
        """Schedules the Job at the given timestamp"""
        args = self.__get_args()
        prio = 1
        for arg in args:
            schedule.enterabs(self.__time, prio, send, argument=arg)
            prio += 1

    def get_time(self) -> datetime:
        return self.__time

    def get_id(self):
        return self.__shelly.id

    def __get_args(self):
        if self.__task == Task.OPEN:
            return [(self.__shelly.set_roller(100),)]
        if self.__task == Task.CLOSE:
            return [(self.__shelly.set_roller(0),)]
        if self.__task == Task.TILT:
            return [(self.__shelly.set_roller(0),), (self.__shelly.set_roller(1), State.CLOSED, self.__shelly)]

    def __repr__(self):
        return 'Job: { time: %s, shelly: %s, task: %s' % (self.__time, self.__shelly, self.__task)