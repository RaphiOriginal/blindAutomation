import logging

from shelly import shelly_finder


def main():
    logging.basicConfig(level=logging.DEBUG)
    shellys = shelly_finder.collect()
    logging.info(shellys)

main()
