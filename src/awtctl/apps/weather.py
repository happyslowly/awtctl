import os
import time

import httpx

from awtctl import AwtrixSDK

LOCATION = os.environ.get("WEATHER_LOCATION", "London")
UNIT = os.environ.get("WEATHER_UNIT", "C")


def fetch_weather() -> tuple[float, str]:
    resp = httpx.get(f"https://wttr.in/{LOCATION}?format=j1", timeout=10)
    resp.raise_for_status()
    data = resp.json()
    current = data["current_condition"][0]
    temp = float(current["temp_C"] if UNIT == "C" else current["temp_F"])
    desc = current["weatherDesc"][0]["value"]
    return temp, desc


def main() -> None:
    sdk = AwtrixSDK(os.environ["AWTRIX_HOST"])
    try:
        while True:
            temp, desc = fetch_weather()
            sdk.create_app(
                "weather",
                text=f"{desc} {temp:.0f}°{UNIT}",
                color="#00BFFF",
                duration=10,
            )
            time.sleep(300)
    finally:
        sdk.delete_app("weather")


if __name__ == "__main__":
    main()
