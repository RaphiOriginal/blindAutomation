#!/usr/bin/env python3
import logging

from shelly import shelly_finder


def main():
    logging.basicConfig(level=logging.INFO)
    walls = shelly_finder.collect()
    logging.info(len(walls))
    logging.info(walls)


main()
