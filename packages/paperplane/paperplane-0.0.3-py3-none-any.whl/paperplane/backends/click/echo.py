import logging
from typing import Optional
from paperplane.backends.click import _secho

logger = logging.getLogger(__name__)


def run(
    prompt: str,
    color: Optional[str] = None,
    fg: Optional[str] = None,
    bg: Optional[str] = None,
    bold: Optional[bool] = False,
):
    if prompt is not None:
        return _secho(message=prompt, fg=color or fg, bg=bg, bold=bold)
    else:
        logger.warning("prompt is None. Nothing to do.")
