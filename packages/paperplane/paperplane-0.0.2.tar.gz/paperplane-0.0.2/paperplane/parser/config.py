import json
import yaml
import copy
import logging
from paperplane.exceptions import ConfigError
from collections import OrderedDict
from typing import List, Dict, OrderedDict as OrderedDictType

logger = logging.getLogger(__name__)

DEFAULT_BACKEND = "click"
top_level_package = __name__.split(".")[0]


def from_yml(yml_string: str) -> dict:
    """Load the given YAML string into a dict

    :param yml_string: YAML string to work on
    :type yml_string: str
    :return: dict representation of the given YAML string
    :rtype: dict
    """
    config: dict = yaml.safe_load(yml_string)
    return config


def from_json(json_string: str) -> dict:
    """Load the given JSON string into a dict

    :param json_string: JSON string to work on
    :type json_string: str
    :return: dict representation of the given JSON string
    :rtype: dict
    """
    try:
        data: dict = json.loads(json_string)
        return data
    except json.JSONDecodeError as e:
        raise ConfigError("Invalid JSON config file") from e


def _validate_and_fix_type(backend: str, key: str, params: dict) -> None:
    """If params.type doesn't specify a backend, modify it to insert the given backend.

    Modifies the params dict in-place.

    :param backend: The backend that should be used if params.type
        doesn't already specify a backend
    :type backend: str
    :param key: Key of the I/O block object
    :type key: str
    :param params: Params for the I/O block object
    :type params: dict
    :return: None
    :rtype: NoneType
    """
    if "type" not in params:
        raise ConfigError(f"Missing 'type' for input {key}")
    if type(params.get("type")) != str:
        raise ConfigError(
            f"'type' for input {key} should be a string datatype. "
            f"Current datatype: {type(params.get('type'))}"
        )
    _type = params.get("type")
    if "." not in _type:
        # Make type = backend.type
        logger.debug(
            f"No backend specified for '{key}'. Using '{backend}' as the backend."
        )
        params["type"] = f"{backend}.{_type}"
    logger.debug(f"Final 'type' param for '{key}' is '{params.get('type')}'")


def _validate_and_fix_prompt(key: str, params: dict) -> None:
    """If no prompt is provided, use "Enter {key}:" as the prompt.

    Modifies the params dict in-place.

    :param key: Key of the I/O block object
    :type key: str
    :param params: Params for the I/O block object
    :type params: dict
    :return: None
    :rtype: NoneType
    """
    if "prompt" not in params:
        params["prompt"] = f"Enter {key}"


def _parse(config: dict) -> OrderedDictType:
    """Validate and parse the config.

    :param config: The config to work upon
    :type config: dict
    :return: A parsed config object
    :rtype: OrderedDict
    """
    logger.debug("Parsing config")
    parsed_config: List[(str, Dict)] = list()

    backend = config.get("backend") or DEFAULT_BACKEND
    logger.debug(f"Using backend {backend}")

    io_blocks: list = config.get("io")
    if io_blocks is None:
        raise ConfigError("Missing key 'io' in config")
    if type(io_blocks) != list:
        raise ConfigError(
            f"'io' block should be a list. Current type: {type(io_blocks)}."
        )
    logger.debug(f"Found {len(io_blocks)} I/O blocks")

    for index, block in enumerate(io_blocks):
        if type(block) != dict:
            raise ConfigError(
                f"'io' block {index} should be a dict. Current type: {type(block)}."
            )
        objects = list(block.items())

        # Invalid: (2 objects in 1 block)
        # inputs:
        # - foo:
        #     bar: baz
        #   qux:
        #     quux: corge

        # Valid: (2 blocks with 1 object each)
        # inputs:
        # - foo:
        #     bar: baz
        # - qux:
        #     quux: corge
        if len(objects) != 1:
            raise ConfigError(
                f"I/O block {index} should contain exactly ONE I/O object. "
                f"Contains: {list(block.keys())}. "
                f"Please split them into multiple blocks."
            )
        key, params = objects[0]
        logger.debug(f"Parsing I/O block object with key '{key}'.")
        if type(params) != dict:
            raise ConfigError(
                f"Parameters for '{key}' should be a dict. Current type: {type(params)}"
            )

        _validate_and_fix_type(backend=backend, key=key, params=params)
        _validate_and_fix_prompt(key=key, params=params)

        backend_module_name = f"{top_level_package}.backends.{params['type']}"

        params_without_type = copy.deepcopy(params)
        del params_without_type["type"]
        parsed_config.append(
            (key, {"backend": backend_module_name, "params": params_without_type})
        )
    return OrderedDict(parsed_config)
