import os
import logging

logger = logging.getLogger(__name__)


def environment(values: str, inputs: dict):
    values = values.split(",")
    for var in values:
        logger.debug(f"Checking if '{var}' environment variable is set.")
        if var in os.environ:
            logger.debug(f"'{var}' environment variable is set!")
            return os.environ.get(var)
        logger.debug(f"'{var}' environment variable is NOT set.")
    return None


def current_working_directory(values: str, inputs: dict):
    logger.debug("Fetching current working directory")
    return os.getcwd()


def context_fetch(values: str, inputs: dict):
    values = values.split(",")
    for var in values:
        logger.debug(f"Checking if '{var}' is set in 'inputs'.")
        if var in inputs:
            res = inputs.get(var)
            logger.debug(f"'{var}' is set in 'inputs' as '{res}'!")
            return res
        logger.debug(f"'{var}' is NOT set in 'inputs'.")
    return None


pattern_mapping = {
    r"(.*)<env:([\w,]*)>(.*)": environment,
    r"(.*)<cwd()>(.*)": current_working_directory,
    r"(.*)<io:([\w,]*)>(.*)": context_fetch,
}
