import sched
import time

from jobs.job import Job
from jobs.jobcollector import Jobcollector
from jobs.task import Task
from meteomatics.meteomatics_api import MeteomaticsAPI
from shelly import shelly_finder

api = MeteomaticsAPI()
sun = api.fetch_sundata()

shellys = shelly_finder.collect()
collector = Jobcollector()

for shelly in shellys:
    collector.add(Job(sun.get_sunrise(), shelly, Task.OPEN))\
        .add(Job(sun.get_sunset(), shelly, Task.CLOSE))\
        .add(Job(sun.find_azimuth(110).time, shelly, Task.TILT))\
        .add(Job(sun.find_azimuth(290).time, shelly, Task.OPEN))

collector.collect().run()
