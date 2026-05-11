import importlib

import click

_APPS: dict[str, str] = {
    "cpu": "awtctl.apps.cpu",
    "fitness": "awtctl.apps.fitness",
    "habit": "awtctl.apps.habit",
    "pomodoro": "awtctl.apps.pomodoro",
    "weather": "awtctl.apps.weather",
}


@click.command(
    "run",
    context_settings={"ignore_unknown_options": True, "allow_extra_args": True},
    help=f"Run a built-in app. Available: {', '.join(sorted(_APPS))}.",
)
@click.argument("app")
@click.argument("app_args", nargs=-1, type=click.UNPROCESSED)
@click.pass_context
def run_cmd(ctx: click.Context, app: str, app_args: tuple[str, ...]) -> None:
    if app not in _APPS:
        available = ", ".join(sorted(_APPS))
        raise click.UsageError(f"Unknown app '{app}'. Available: {available}")
    mod = importlib.import_module(_APPS[app])
    mod.main(host=ctx.obj["host"], args=list(app_args))
