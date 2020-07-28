#!/usr/bin/env python3
import logging

from shelly import shelly_finder


def main():
    logging.basicConfig(level=logging.INFO)
    shellys = shelly_finder.collect()
    logging.info(len(shellys))
    logging.info(shellys)


main()
