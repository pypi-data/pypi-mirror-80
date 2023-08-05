import click
import logging
import sys
import json as _json
import pprint
from paperplane.parser.config import from_yml, from_json
from paperplane.parser.main import parse_and_execute

top_level_package = __name__.split(".")[0]
package_root_logger = logging.getLogger(top_level_package)


@click.group()
@click.option("--debug/--no-debug", default=False)
@click.pass_context
def cli(ctx, debug):
    if debug:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        package_root_logger.addHandler(handler)
        package_root_logger.setLevel(logging.DEBUG)

    ctx.ensure_object(dict)
    ctx.obj["DEBUG"] = debug


@cli.command()
@click.option(
    "--format",
    help="Format of the COFNIG_FILE",
    default="YAML",
    type=click.Choice(["JSON", "YAML"], case_sensitive=False),
)
@click.option(
    "--json-out/--no-json-out",
    help="Should the output be a JSON object instead of a Python dict",
    default=False,
)
@click.argument("config_file", type=click.File("rb"))
@click.pass_context
def collect(ctx, config_file, format: str, json_out: bool):
    format = format.upper()
    if format == "JSON":
        config = from_json(config_file.read())
    elif format == "YAML":
        config = from_yml(config_file.read())
    else:
        raise ValueError(f"Unknown format {format}")
    values = parse_and_execute(config)
    click.secho("Collected inputs:", fg="green")
    if json_out:
        print(_json.dumps(values, indent=2))
    else:
        pprint.pprint(values, indent=2)
