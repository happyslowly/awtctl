import argparse
import os
import time

from awtctl import AwtrixSDK


def countdown(sdk: AwtrixSDK, label: str, color: str, seconds: int) -> None:
    for remaining in range(seconds, 0, -1):
        sdk.create_app(
            "fitness",
            text=f"{label} {remaining:02d}",
            color=color,
            progress=int((1 - remaining / seconds) * 100),
            progress_c=color,
            progress_bc="#1A1A1A",
            duration=2,
        )
        sdk.switch_app("fitness")
        time.sleep(1)


def main() -> None:
    parser = argparse.ArgumentParser(description="HIIT interval timer on AWTRIX.")
    parser.add_argument(
        "--rounds", type=int, default=8, help="Number of rounds (default 8)."
    )
    parser.add_argument(
        "--work", type=int, default=30, help="Work duration in seconds (default 30)."
    )
    parser.add_argument(
        "--rest", type=int, default=10, help="Rest duration in seconds (default 10)."
    )
    parser.add_argument(
        "--prepare",
        type=int,
        default=0,
        help="Initial get-ready countdown in seconds (default off).",
    )
    args = parser.parse_args()

    sdk = AwtrixSDK(os.environ["AWTRIX_HOST"])
    sdk.update_settings(blockn=True, atrans=False)

    try:
        if args.prepare:
            countdown(sdk, "READY", "#FF8000", args.prepare)

        for round_num in range(1, args.rounds + 1):
            sdk.create_app(
                "fitness",
                text=f"R{round_num}/{args.rounds}",
                color="#FF8000",
                duration=3,
            )
            sdk.switch_app("fitness")
            time.sleep(3)
            countdown(sdk, "WORK", "#FF0000", args.work)
            if round_num < args.rounds:
                countdown(sdk, "REST", "#00FF00", args.rest)

        sdk.notify("Workout done!", color="#00FF00", duration=15, wakeup=True)
    finally:
        sdk.delete_app("fitness")
        sdk.update_settings(blockn=False, atrans=True)


if __name__ == "__main__":
    main()
