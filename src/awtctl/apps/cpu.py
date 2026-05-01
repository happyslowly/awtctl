import os
import time

import psutil

from awtctl import AwtrixSDK


def main() -> None:
    sdk = AwtrixSDK(os.environ["AWTRIX_HOST"])
    try:
        while True:
            cpu = psutil.cpu_percent(interval=1)
            sdk.create_app(
                "cpu",
                text=f"CPU {cpu:.0f}%",
                progress=int(cpu),
                progress_c="#FF8000",
                progress_bc="#1A1A1A",
                duration=10,
            )
            time.sleep(5)
    finally:
        sdk.delete_app("cpu")


if __name__ == "__main__":
    main()
