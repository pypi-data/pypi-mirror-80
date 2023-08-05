import click
from typing import Any, Optional
from paperplane.backends.click import _prompt


def run(prompt: str, choices: list, default: Optional[Any] = None):
    return _prompt(text=prompt, default=default, type=click.Choice(choices=choices))
