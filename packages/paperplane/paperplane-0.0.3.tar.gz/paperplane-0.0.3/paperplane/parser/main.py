import logging
import re
import importlib
from typing import Any, Optional, Dict
from paperplane.exceptions import BackendError, ConfigError
from paperplane.parser.config import _parse
from paperplane.parser.macros import pattern_mapping

logger = logging.getLogger(__name__)


def _expand_macro(key: str, params: dict, param_key: str, inputs: dict) -> None:
    """
    Expand `params.<param_key>` if it contains a known macro.

    Modifies the params dict in-place.

    :param key: Key of the I/O block object
    :type key: str
    :param params: Params for the I/O block object
    :type params: dict
    :param param_key: The key in params to check/expand macros for
    :type param_key: str
    :param inputs: Input values collected so far
    :type inputs: dict
    :return: None
    :rtype: NoneType
    """

    logger.debug(f"Checking if '{key}.{param_key}' contains a macro")
    if param_key not in params or params.get(param_key) is None:
        logger.debug(f"'{key}.{param_key}' is missing or is None. No macros to expand.")
        return
    param_value: Optional[str] = params.get(param_key)
    if type(param_value) != str:
        logger.debug(
            f"'{key}.{param_key}' is not a string "
            f"(it is of type '{type(param_value)}'). No macros to expand."
        )
        return
    match_count = 0
    for pattern, _callable in pattern_mapping.items():
        logger.info(f"Searching for '{pattern}' macros for '{key}.{param_key}'")
        match = re.search(pattern, param_value)
        while match:
            match_count += 1
            logger.info(
                f"Found macro for '{key}.{param_key}': "
                f"'{param_value}'. Expanding..."
            )
            macro_value = _callable(values=match.group(2), inputs=inputs)
            if macro_value is not None:
                param_value = re.sub(pattern, rf"\g<1>{macro_value}\g<3>", param_value)
                logger.info(
                    f"Expanded macro for '{key}.{param_key}': " f"'{param_value}'."
                )
            else:
                param_value = None
                logger.warning(
                    f"Macro for '{key}.{param_key}' returned None. "
                    f"Setting '{key}.{param_key}' to None."
                )
            if param_value is None:
                # Break loop
                logger.debug(
                    f"Stopping macro search for pattern {pattern} "
                    f"for '{key}.{param_key}'"
                )
                match = False
            else:
                match = re.search(pattern, param_value)
    if match_count == 0:
        logger.info(f"No macros found for '{key}.{param_key}'.")
    else:
        params[param_key] = param_value


def _execute(backend_module_name: str, **kwargs) -> Any:
    """Invoke `run` method of the specified module with the given keyword arguments

    :param backend_module_name: Name of the module to import and invoke
        the `run` method of
    :type backend_module_name: str
    :param kwargs: Keyword arguments to pass to the `run` method
    :type kwargs: Any
    :return: The value returned by the `run` method of the given module
    :rtype: Any
    """
    try:
        module = importlib.import_module(backend_module_name)
    except ModuleNotFoundError as e:
        raise BackendError(f"Unknown backend {backend_module_name}") from e

    if not hasattr(module, "run") or not callable(module.run):
        raise BackendError(
            f"Backend {backend_module_name} does not have a callable run() method"
        )

    try:
        value = module.run(**kwargs)
    except TypeError as e:
        raise ConfigError(e) from e

    return value


def parse_and_execute(config: dict) -> Dict[str, Any]:
    """Validate, parse and transform the config. Execute backends based
    on the transformed config to perform I/O operations.

    If `prompt` and/or `default` contains a macro, it will be expanded.

    :param config: The original config
    :type config: dict
    :return: A dict containing values collected during I/O operations for the
        corresponding key
    :rtype: dict
    """
    parsed_config = _parse(config)
    res: Dict[str, Any] = dict()
    for key, value in parsed_config.items():
        backend = value.get("backend")
        params = value.get("params")

        # TODO: Maybe use Jinja2 template rendering instead of macro expansion?
        _expand_macro(key=key, params=params, param_key="prompt", inputs=res)
        _expand_macro(key=key, params=params, param_key="default", inputs=res)
        res[key] = _execute(backend_module_name=backend, **params)
    return res
