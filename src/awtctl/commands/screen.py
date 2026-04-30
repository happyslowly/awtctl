import click


def _render_screen(pixels: list[int], width: int = 32) -> None:
    for i, color in enumerate(pixels):
        r = (color >> 16) & 0xFF
        g = (color >> 8) & 0xFF
        b = color & 0xFF
        print(f"\033[48;2;{r};{g};{b}m  \033[0m", end="")
        if (i + 1) % width == 0:
            print()


@click.command(help="Render current matrix screen in terminal.")
@click.pass_context
def screen(ctx: click.Context) -> None:
    pixels = ctx.obj["client"].get("screen")
    _render_screen(pixels)
