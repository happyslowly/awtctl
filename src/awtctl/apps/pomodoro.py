import argparse
import os
import time

from awtctl import AwtrixSDK


def main(host: str | None = None, args: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Pomodoro timer on AWTRIX.")
    parser.add_argument(
        "minutes",
        type=int,
        nargs="?",
        default=25,
        help="Duration in minutes (default 25).",
    )
    parsed = parser.parse_args(args)

    total = parsed.minutes * 60
    sdk = AwtrixSDK(host or os.environ["AWTRIX_HOST"])

    sdk.update_settings(blockn=True, atrans=False)
    try:
        remaining = total
        while remaining > 0:
            mins, secs = divmod(remaining, 60)
            sdk.create_app(
                "pomodoro",
                text=f"{mins:02d}:{secs:02d}",
                color="#FF0000",
                progress=int((1 - remaining / total) * 100),
                progress_c="#FF0000",
                progress_bc="#1A1A1A",
                duration=2,
            )
            sdk.switch_app("pomodoro")
            time.sleep(1)
            remaining -= 1

        sdk.notify(
            "Pomodoro done! Take a break.",
            color="#00FF00",
            duration=10,
            wakeup=True,
        )
    finally:
        sdk.delete_app("pomodoro")
        sdk.update_settings(blockn=False, atrans=True)


if __name__ == "__main__":
    main()
