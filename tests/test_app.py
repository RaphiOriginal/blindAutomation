#!/usr/bin/env python3
from jobs.job import Job
from jobs.jobmanager import JobManager
from jobs.task import Task
from shelly import shelly_finder
from tests.mock.mocks import get_sundata_mock


def main():
    sun = get_sundata_mock()

    shellys = shelly_finder.collect()
    manager = JobManager()

    for shelly in shellys:
        manager.add(Job(sun.get_sunrise(), shelly, Task.OPEN)) \
            .add(Job(sun.get_sunset(), shelly, Task.CLOSE)) \
            .add(Job(sun.find_azimuth(110).time, shelly, Task.TILT)) \
            .add(Job(sun.find_azimuth(290).time, shelly, Task.OPEN))

    manager.prepare().run()


main()
