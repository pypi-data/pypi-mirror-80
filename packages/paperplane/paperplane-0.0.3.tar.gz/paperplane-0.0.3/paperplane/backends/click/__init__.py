import click


def _prompt(*args, **kwargs):
    return click.prompt(*args, **kwargs)


def _secho(*args, **kwargs):
    return click.secho(*args, **kwargs)
