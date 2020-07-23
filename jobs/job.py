from datetime import datetime
import sched
import time

from jobs.request_task import Requesttask
from jobs.task import Task
from shelly.shelly import Shelly


class Job:
    def __init__(self, time: datetime, shelly: Shelly, task: Task):
        self.__time: datetime = time
        self.__shelly: Shelly = shelly
        self.__task: Task = task

    def schedule(self):
        schedule = sched.scheduler(time.time)
        delay = self.__calculate_delay()
        schedule.enter(delay.seconds, 1, Requesttask(self.__get_task()).run())
        schedule.run()

    def __calculate_delay(self):
        now = datetime.now(self.__time.timetz())
        return self.__time - now

    def __get_task(self):
        if self.__task == Task.OPEN:
            return self.__shelly.setRoller(100)
        if self.__task == Task.CLOSE:
            return self.__shelly.setRoller(0)
        if self.__task == Task.TILT:
            return self.__shelly.setRoller(1)
