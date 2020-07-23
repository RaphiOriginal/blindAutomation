import sched
import time
from datetime import datetime, timedelta
from time import sleep

import requests

from jobs.job import Job
from jobs.task import Task
from meteomatics.meteomatics_api import MeteomaticsAPI
from shelly import shelly_finder

#api = MeteomaticsAPI()
#(sunrise, sunset) = api.getSunriseAndSunset()
#print(api.getAzimuthTime(sunrise, sunset, 110.0))
#print(api.getAzimuthTime(sunrise, sunset, 290.0))

shellys = shelly_finder.collect()

now = datetime.now()
delta = timedelta(seconds=5)

shelly = shellys[0]
schedule = sched.scheduler(time.time)
job = Job(now + delta, shelly, Task.TILT)
job.schedule(schedule)
schedule.run()
print(now)
