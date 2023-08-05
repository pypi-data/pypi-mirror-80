import click
from typing import Optional
from paperplane.backends.click import _prompt


def run(prompt: str, default: Optional[int] = None):
    return _prompt(text=prompt, default=default, type=click.INT)
