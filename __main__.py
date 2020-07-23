import sched
import time

from jobs.job import Job
from jobs.task import Task
from meteomatics.meteomatics_api import MeteomaticsAPI
from shelly import shelly_finder

api = MeteomaticsAPI()
sun = api.get_sundata()

shellys = shelly_finder.collect()
schedule = sched.scheduler(time.time)

for shelly in shellys:
    Job(sun.get_sunrise(), shelly, Task.OPEN).schedule(schedule)
    Job(sun.get_sunset(), shelly, Task.CLOSE).schedule(schedule)
    Job(sun.find_azimuth(110).time, shelly, Task.TILT).schedule(schedule)
    Job(sun.find_azimuth(290).time, shelly, Task.OPEN).schedule(schedule)

schedule.run()
