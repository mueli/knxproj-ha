#!/usr/bin/env python3
import logging
import argparse
from pathlib import Path
import sys
import io

xknxproj_dp = "/Users/mueli/VCS/xknxproject"
sys.path.insert(0, xknxproj_dp)
from xknxproject.models import KNXProject
from xknxproject import XKNXProj

logger = logging.getLogger('convert')


def load_project(fp: Path, language: str = "de-DE") -> XKNXProj:
    """Load the xknx project

    Args:
        fp (Path): file path to the knx project (*.knxproj)
        language (str, optional): Language code to be used. Defaults to "de-DE".

    Returns:
        XKNXProj: the parsed knxproj content
    """
    knxproj: XKNXProj = XKNXProj(
        path=fp,
        language="de-DE",  # optional
    )
    logger.debug("Start parsing KNX project file ...")
    project: KNXProject = knxproj.parse()
    logger.debug("  ... parsing finished")
    return project


def grep_config(comment: str) -> str:
    """Grep the hassio config from the comment

    Is searching for any text content within the following begin and end lines

    ```hassio
    <config>
    ```

    Args:
        comment (str): pure text (NO RTF) comment string 

    Returns:
        str: actual hassio config
    """
    config = ""
    buff = io.StringIO(comment)
    # Will fetch first occurence only ...
    for _ in iter(buff.readline, "```hassio\n"):
        pass
    for line in iter(buff.readline, "```\n"):
        config += line
    return config


def main():
    parser = argparse.ArgumentParser(prog="knx-project-converter")
    parser.add_argument("-d", "--debug", action="store_true")
    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    p = load_project("resources/private.knxproj")

    for ga in p["group_addresses"]:
        if p["group_addresses"][ga]['comment']:
            config = grep_config(p["group_addresses"][ga]['comment'])
            logger.debug(f"’{p['group_addresses'][ga]['address']}’: '{config}'")


if __name__ == "__main__":
    main()
