import json

import click


@click.command(name="dismiss", help="Dismiss the current held notification.")
@click.pass_context
def dismiss(ctx: click.Context) -> None:
    ctx.obj["sdk"].dismiss_notification()
    print("Dismissed.")


@click.command(name="send", help="Send a notification.")
@click.argument("text", required=False)
@click.option("--text-case", type=int, default=None, help="0=global, 1=uppercase, 2=as-sent.")
@click.option("--top-text", is_flag=True, default=False, help="Draw text on top.")
@click.option("--text-offset", type=int, default=None, help="X position offset for text.")
@click.option("--no-center", is_flag=True, default=False, help="Disable text centering.")
@click.option("--color", "-c", default=None, help="Text color as hex (#FF0000) or R,G,B.")
@click.option("--gradient", default=None, help="Two-color gradient as JSON array.")
@click.option("--blink-text", type=int, default=None, help="Blink interval in ms.")
@click.option("--fade-text", type=int, default=None, help="Fade interval in ms.")
@click.option("--background", default=None, help="Background color as hex or R,G,B.")
@click.option("--rainbow", is_flag=True, default=False, help="Cycle each letter through RGB spectrum.")
@click.option("--icon", "-i", default=None, help="Icon ID, filename, or Base64 8x8 JPG.")
@click.option("--push-icon", type=int, default=None, help="0=static, 1=moves once, 2=repeats.")
@click.option("--repeat", type=int, default=None, help="Times to scroll text before ending.")
@click.option("--duration", "-d", type=int, default=None, help="Display duration in seconds.")
@click.option("--hold", is_flag=True, default=False, help="Hold until dismissed via button or API.")
@click.option("--sound", default=None, help="RTTTL melody filename (without extension).")
@click.option("--rtttl", default=None, help="Inline RTTTL sound string.")
@click.option("--loop-sound", is_flag=True, default=False, help="Loop sound for notification duration.")
@click.option("--bar", default=None, help="Bar graph values as JSON array, e.g. '[1,2,3]'.")
@click.option("--line", default=None, help="Line chart values as JSON array, e.g. '[1,2,3]'.")
@click.option("--no-autoscale", is_flag=True, default=False, help="Disable autoscaling for bar/line.")
@click.option("--bar-bc", default=None, help="Bar background color.")
@click.option("--progress", type=int, default=None, help="Progress bar value 0-100.")
@click.option("--progress-c", default=None, help="Progress bar color.")
@click.option("--progress-bc", default=None, help="Progress bar background color.")
@click.option("--draw", default=None, help="Drawing instructions as JSON array.")
@click.option("--no-stack", is_flag=True, default=False, help="Replace current notification immediately.")
@click.option("--wakeup", is_flag=True, default=False, help="Wake matrix if off.")
@click.option("--no-scroll", is_flag=True, default=False, help="Disable text scrolling.")
@click.option("--clients", default=None, help="Forward to other AWTRIX devices as JSON array.")
@click.option("--scroll-speed", type=int, default=None, help="Scroll speed as percentage (default 100).")
@click.option("--effect", default=None, help="Background effect name.")
@click.option("--effect-settings", default=None, help="Effect color/speed settings as JSON.")
@click.option("--overlay", default=None, help="Overlay effect (snow, rain, drizzle, storm, thunder, frost).")
@click.pass_context
def send(
    ctx: click.Context,
    text: str | None,
    text_case: int | None,
    top_text: bool,
    text_offset: int | None,
    no_center: bool,
    color: str | None,
    gradient: str | None,
    blink_text: int | None,
    fade_text: int | None,
    background: str | None,
    rainbow: bool,
    icon: str | None,
    push_icon: int | None,
    repeat: int | None,
    duration: int | None,
    hold: bool,
    sound: str | None,
    rtttl: str | None,
    loop_sound: bool,
    bar: str | None,
    line: str | None,
    no_autoscale: bool,
    bar_bc: str | None,
    progress: int | None,
    progress_c: str | None,
    progress_bc: str | None,
    draw: str | None,
    no_stack: bool,
    wakeup: bool,
    no_scroll: bool,
    clients: str | None,
    scroll_speed: int | None,
    effect: str | None,
    effect_settings: str | None,
    overlay: str | None,
) -> None:
    ctx.obj["sdk"].notify(
        text,
        text_case=text_case,
        top_text=top_text,
        text_offset=text_offset,
        center=not no_center,
        color=color,
        gradient=json.loads(gradient) if gradient else None,
        blink_text=blink_text,
        fade_text=fade_text,
        background=background,
        rainbow=rainbow,
        icon=icon,
        push_icon=push_icon,
        repeat=repeat,
        duration=duration,
        hold=hold,
        sound=sound,
        rtttl=rtttl,
        loop_sound=loop_sound,
        bar=json.loads(bar) if bar else None,
        line=json.loads(line) if line else None,
        autoscale=not no_autoscale,
        bar_bc=bar_bc,
        progress=progress,
        progress_c=progress_c,
        progress_bc=progress_bc,
        draw=json.loads(draw) if draw else None,
        stack=not no_stack,
        wakeup=wakeup,
        scroll=not no_scroll,
        clients=json.loads(clients) if clients else None,
        scroll_speed=scroll_speed,
        effect=effect,
        effect_settings=json.loads(effect_settings) if effect_settings else None,
        overlay=overlay,
    )
    print("Sent.")
