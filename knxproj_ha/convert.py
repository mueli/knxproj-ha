import logging
from pathlib import Path
import io
from xknxproject.models import KNXProject
from xknxproject import XKNXProj
from .models import HAConfig, Entity, Light
import yaml


logger = logging.getLogger("knxproj_ha")


def _grep_config(comment: str) -> str:
    """Grep the hassio config from the comment

    Is searching for any text content within the following begin and end lines

    ```hassos
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
    for line in iter(buff.readline, "```hassos\n"):
        if not line:
            break
        pass
    for line in iter(buff.readline, "```\n"):
        if not line:
            break
        config += line
    return config


def _create_entity(config: dict, ga: dict) -> Entity:
    """Create an Home Assistant configuration entity from config"""
    if len(config.keys()) > 1:
        raise ValueError(
            f"There can be only one device type for a given Ga, "
            f"but received '{config.keys()}'"
        )
    device_type = next(iter(config))
    logger.debug(f"Found device type '{device_type}'")
    params = config[device_type] if config[device_type] else {}
    if device_type == "light":
        entity = Light(
            name=params["name"] if "name" in params else ga["name"],
            address=ga["address"],
            state_address=ga["address"],
        )
    return entity


def convert(fp: Path, language: str = "de-DE") -> HAConfig:
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
    ha_config = HAConfig()
    for ga in project["group_addresses"]:
        if project["group_addresses"][ga]["comment"]:
            config_str = _grep_config(project["group_addresses"][ga]["comment"])
            if config_str:
                config = yaml.safe_load(config_str)
                entity = _create_entity(config, project["group_addresses"][ga])
                getattr(ha_config, entity._type_id).append(entity)
    return ha_config


def write(ha_config: HAConfig, dp: Path) -> None:
    """Serialize the given Home Assistant into the provided directory path"""
    print(yaml.dump(ha_config.model_dump(), indent=2))
