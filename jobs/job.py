from datetime import datetime, timedelta
from sched import scheduler

from jobs.send import send
from jobs.task import Task
from shelly.shelly import Shelly


class Job:
    def __init__(self, time: datetime, shelly: Shelly, task: Task):
        self.__time: datetime = time
        self.__shelly: Shelly = shelly
        self.__task: Task = task
        self.__delay = timedelta(seconds=25)

        print('{}: Job for {} to {} created with {}'.format(datetime.now(), time, task, shelly))

    def schedule(self, schedule: scheduler):
        delay = self.__calculate_delay()
        urls = self.__get_urls()
        for url in urls:
            schedule.enter(delay.seconds, 1, send, argument=(url,))
            delay = delay + self.__delay

    def __calculate_delay(self):
        now = datetime.now(self.__time.tzinfo)
        return self.__time - now

    def __get_urls(self):
        if self.__task == Task.OPEN:
            return [self.__shelly.setRoller(100)]
        if self.__task == Task.CLOSE:
            return [self.__shelly.setRoller(0)]
        if self.__task == Task.TILT:
            return [self.__shelly.setRoller(0), self.__shelly.setRoller(1)]
