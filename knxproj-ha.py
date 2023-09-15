#!/usr/bin/env python3
import logging
import argparse
from knxproj_ha.convert import convert

logger = logging.getLogger("convert")


def main():
    parser = argparse.ArgumentParser(prog="knx-project-converter")
    parser.add_argument("-d", "--debug", action="store_true")
    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    p = convert("resources/private.knxproj")


if __name__ == "__main__":
    main()
