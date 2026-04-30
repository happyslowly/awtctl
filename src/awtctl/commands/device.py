import click


@click.command(help="Turn the matrix on or off.")
@click.argument("state", type=click.Choice(["on", "off"]))
@click.pass_context
def power(ctx: click.Context, state: str) -> None:
    ctx.obj["client"].post("power", {"power": state == "on"})
    print("Done.")


@click.command(help="Put the device into deep sleep for X seconds.")
@click.argument("seconds", type=int)
@click.pass_context
def sleep(ctx: click.Context, seconds: int) -> None:
    ctx.obj["client"].post("sleep", {"sleep": seconds})
    print("Sleeping.")


@click.command(help="Trigger a firmware update.")
@click.pass_context
def update(ctx: click.Context) -> None:
    ctx.obj["client"].post("doupdate", {})
    print("Update triggered.")


@click.command(help="Reboot the device.")
@click.confirmation_option(prompt="Reboot the device?")
@click.pass_context
def reboot(ctx: click.Context) -> None:
    ctx.obj["client"].post("reboot", {})
    print("Rebooting.")
