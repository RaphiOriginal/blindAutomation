from datetime import datetime, timedelta
from sched import scheduler

from jobs.request_task import Requesttask
from jobs.task import Task
from shelly.shelly import Shelly


class Job:
    def __init__(self, time: datetime, shelly: Shelly, task: Task):
        self.__time: datetime = time
        self.__shelly: Shelly = shelly
        self.__task: Task = task
        self.__delay = timedelta(seconds=25)

    def schedule(self, schedule: scheduler):
        delay = self.__calculate_delay()
        tasks = self.__get_task()
        for task in tasks:
            schedule.enter(delay.seconds, 1, Requesttask(task).run())
            delay = delay + self.__delay

    def __calculate_delay(self):
        now = datetime.now(self.__time.tzinfo)
        return self.__time - now

    def __get_task(self):
        if self.__task == Task.OPEN:
            return [self.__shelly.setRoller(100)]
        if self.__task == Task.CLOSE:
            return [self.__shelly.setRoller(0)]
        if self.__task == Task.TILT:
            return [self.__shelly.setRoller(0), self.__shelly.setRoller(1)]
