#!/usr/bin/env python3
import logging
import argparse
from knxproj_ha.convert import convert, write

logger = logging.getLogger("convert")


def main():
    parser = argparse.ArgumentParser(prog="knx-project-converter")
    parser.add_argument("-d", "--debug", action="store_true")
    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    ha_config = convert("resources/private.knxproj")
    write(ha_config, "")


if __name__ == "__main__":
    main()
