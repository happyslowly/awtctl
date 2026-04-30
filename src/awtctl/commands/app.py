import json
from pathlib import Path

import click
import yaml

BUILTIN_APPS = ["Time", "Date", "Temperature", "Humidity", "Battery"]


@click.command(help="Create or update a custom app from a JSON or YAML file.")
@click.argument("name")
@click.argument("file", type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.pass_context
def create(ctx: click.Context, name: str, file: Path) -> None:
    content = file.read_text()
    if file.suffix in (".yaml", ".yml"):
        payload = yaml.safe_load(content)
    else:
        payload = json.loads(content)
    ctx.obj["client"].post(f"custom?name={name}", payload)
    print("Done.")


@click.command(help="Switch to a specific app by name.")
@click.argument("name")
@click.pass_context
def switch(ctx: click.Context, name: str) -> None:
    ctx.obj["client"].post("switch", {"name": name})


@click.command(help=f"Go to the next app. Built-in apps: {', '.join(BUILTIN_APPS)}.")
@click.pass_context
def next(ctx: click.Context) -> None:
    ctx.obj["client"].post("nextapp", {})


@click.command(help="Go to the previous app.")
@click.pass_context
def prev(ctx: click.Context) -> None:
    ctx.obj["client"].post("previousapp", {})
