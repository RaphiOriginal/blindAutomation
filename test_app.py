#!/usr/bin/env python3
from jobs import trigger
from jobs.jobmanager import JobManager
from shelly import shelly_finder
from tests.mock.mocks import get_sundata_mock


def main():
    sun = get_sundata_mock()

    shellys = shelly_finder.collect()
    manager = JobManager()

    for shelly in shellys:
        trigger.apply_triggers(manager, sun, shelly)

    manager.prepare().run()


main()
