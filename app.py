#!/usr/bin/env python3
import logging

from jobs import trigger
from jobs.jobmanager import JobManager
from meteomatics.meteomatics_api import MeteomaticsAPI
from shelly import shelly_finder


logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(level=logging.DEBUG)
    api = MeteomaticsAPI()
    shellys = shelly_finder.collect()
    sun = api.fetch_sundata()

    manager = JobManager()

    for shelly in shellys:
        trigger.apply_triggers(manager, sun, shelly)

    manager.prepare().run()


main()
