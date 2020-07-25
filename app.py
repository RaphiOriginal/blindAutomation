#!/usr/bin/env python3
from jobs.job import Job
from jobs.jobmanager import JobManager
from jobs.task import Task
from jobs.trigger import SunriseTrigger, SunsetTrigger, SunInTrigger, SunOutTrigger
from meteomatics.meteomatics_api import MeteomaticsAPI
from shelly import shelly_finder


def main():
    api = MeteomaticsAPI()
    sun = api.fetch_sundata()

    shellys = shelly_finder.collect()
    manager = JobManager()

    for shelly in shellys:
        manager.add(Job(SunriseTrigger(sun), shelly)) \
            .add(Job(SunsetTrigger(sun), shelly)) \
            .add(Job(SunInTrigger(sun, 110), shelly)) \
            .add(Job(SunOutTrigger(sun, 290), shelly))

    manager.prepare().run()


main()
