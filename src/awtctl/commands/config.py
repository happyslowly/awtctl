import json

import click


@click.group(help="Get or update device configuration.")
def config() -> None:
    pass


@config.command(name="get", help="Print current configuration.")
@click.pass_context
def config_get(ctx: click.Context) -> None:
    print(json.dumps(ctx.obj["sdk"].get_settings(), indent=2))


@config.command(name="set", help="Update one or more settings. Values are parsed as JSON (e.g. BRI=128 UPPERCASE=false TCOL='#FF8000').")
@click.argument("pairs", nargs=-1, required=True)
@click.pass_context
def config_set(ctx: click.Context, pairs: tuple[str, ...]) -> None:
    kwargs: dict = {}
    for pair in pairs:
        if "=" not in pair:
            raise click.BadParameter(f"Expected KEY=VALUE, got: {pair}")
        key, _, raw = pair.partition("=")
        try:
            kwargs[key] = json.loads(raw)
        except json.JSONDecodeError:
            kwargs[key] = raw
    ctx.obj["sdk"].update_settings(**kwargs)
    print("Done.")


@config.command(name="reset", help="Reset all settings to defaults (does not affect WiFi or flash files).")
@click.confirmation_option(prompt="This will reset all settings. Continue?")
@click.pass_context
def config_reset(ctx: click.Context) -> None:
    ctx.obj["sdk"].reset_settings()
    print("Reset.")
