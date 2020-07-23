from datetime import datetime
from sched import scheduler

from jobs.send import send
from jobs.task import Task
from shelly.shelly import Shelly


class Job:
    def __init__(self, time: datetime, shelly: Shelly, task: Task):
        self.__time: datetime = time
        self.__shelly: Shelly = shelly
        self.__task: Task = task

        print('{}: Job for {} to {} created with {}'.format(datetime.now(), time, task, shelly))

    def schedule(self, schedule: scheduler):
        delay = self.__calculate_delay()
        args = self.__get_args()
        for arg in args:
            schedule.enter(delay.seconds, 1, send, argument=arg)

    def __calculate_delay(self):
        now = datetime.now(self.__time.tzinfo)
        return self.__time - now

    def __get_args(self):
        if self.__task == Task.OPEN:
            return [(self.__shelly.set_roller(100),)]
        if self.__task == Task.CLOSE:
            return [(self.__shelly.set_roller(0),)]
        if self.__task == Task.TILT:
            return [(self.__shelly.set_roller(0),), (self.__shelly.set_roller(1), 0, self.__shelly.get_roller())]
