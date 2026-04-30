import json

import click


@click.group(invoke_without_command=True, help="Device stats.")
@click.pass_context
def stats(ctx: click.Context) -> None:
    if ctx.invoked_subcommand is None:
        data = ctx.obj["client"].get("stats")
        print(json.dumps(data, indent=2))


@stats.command(name="effects", help="List all available effects.")
@click.pass_context
def stats_effects(ctx: click.Context) -> None:
    data = ctx.obj["client"].get("effects")
    print(json.dumps(data, indent=2))


@stats.command(name="transitions", help="List all available transition effects.")
@click.pass_context
def stats_transitions(ctx: click.Context) -> None:
    data = ctx.obj["client"].get("transitions")
    print(json.dumps(data, indent=2))


@stats.command(name="loop", help="List all apps in the loop.")
@click.pass_context
def stats_loop(ctx: click.Context) -> None:
    data = ctx.obj["client"].get("loop")
    print(json.dumps(data, indent=2))
