import click

from awtctl.sdk import AwtrixSDK
from awtctl.commands.app import create, next, prev, switch
from awtctl.commands.config import config
from awtctl.commands.device import power, reboot, sleep, update
from awtctl.commands.notify import dismiss, send
from awtctl.commands.screen import screen
from awtctl.commands.stats import stats


@click.group()
@click.option("--host", envvar="AWTRIX_HOST", default=None)
@click.pass_context
def cli(ctx: click.Context, host: str | None) -> None:
    if not host:
        raise click.UsageError(
            "Host is required. Use --host or set the AWTRIX_HOST environment variable."
        )
    ctx.ensure_object(dict)
    ctx.obj["sdk"] = AwtrixSDK(host)


cli.add_command(stats)
cli.add_command(screen)
cli.add_command(power)
cli.add_command(sleep)
cli.add_command(update)
cli.add_command(reboot)
cli.add_command(create)
cli.add_command(switch)
cli.add_command(next)
cli.add_command(prev)
cli.add_command(send)
cli.add_command(dismiss)
cli.add_command(config)


if __name__ == "__main__":
    cli()
