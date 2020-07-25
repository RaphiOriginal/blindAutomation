#!/usr/bin/env python3
from jobs.job import Job
from jobs.jobmanager import JobManager
from jobs.trigger import SunriseTrigger, SunsetTrigger, SunInTrigger, SunOutTrigger
from shelly import shelly_finder
from tests.mock.mocks import get_sundata_mock


def main():
    sun = get_sundata_mock()

    shellys = shelly_finder.collect()
    manager = JobManager()

    for shelly in shellys:
        manager.add(Job(SunriseTrigger(sun), shelly)) \
            .add(Job(SunsetTrigger(sun), shelly)) \
            .add(Job(SunInTrigger(sun, 110), shelly)) \
            .add(Job(SunOutTrigger(sun, 290), shelly))

    manager.prepare().run()


main()
