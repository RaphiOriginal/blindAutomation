import sched
import time

from jobs.job import Job
from jobs.task import Task
from meteomatics.meteomatics_api import MeteomaticsAPI
from shelly import shelly_finder

api = MeteomaticsAPI()
(sunrise, sunset) = api.get_sunrise_and_sunset()
tilt = api.get_azimuth_time(sunrise, sunset, 110.0)
up = api.get_azimuth_time(sunrise, sunset, 290.0)

shellys = shelly_finder.collect()
schedule = sched.scheduler(time.time)

for shelly in shellys:
    Job(sunrise, shelly, Task.OPEN).schedule(schedule)
    Job(sunset, shelly, Task.CLOSE).schedule(schedule)
    Job(tilt, shelly, Task.TILT).schedule(schedule)
    Job(up, shelly, Task.OPEN).schedule(schedule)

schedule.run()
