import argparse
import os
import signal
import sys
import threading
import httpx

from awtctl import AwtrixSDK

_WMO: dict[int, str] = {
    0: "Clear",
    1: "Mainly Clear", 2: "Partly Cloudy", 3: "Overcast",
    45: "Fog", 48: "Icy Fog",
    51: "Lt Drizzle", 53: "Drizzle", 55: "Hv Drizzle",
    61: "Lt Rain", 63: "Rain", 65: "Hv Rain",
    71: "Lt Snow", 73: "Snow", 75: "Hv Snow",
    77: "Snow Grains",
    80: "Lt Showers", 81: "Showers", 82: "Hv Showers",
    85: "Snow Showers", 86: "Hv Snow Showers",
    95: "Thunderstorm", 96: "Tstorm+Hail", 99: "Tstorm+Hail",
}


def _geocode(location: str) -> tuple[float, float]:
    resp = httpx.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={"name": location, "count": 1},
        timeout=10,
    )
    resp.raise_for_status()
    results = resp.json().get("results", [])
    if not results:
        raise ValueError(f"Location not found: {location}")
    return results[0]["latitude"], results[0]["longitude"]


def _fetch(lat: float, lon: float, unit: str) -> tuple[float, str]:
    resp = httpx.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": lat,
            "longitude": lon,
            "current": "temperature_2m,weathercode",
            "temperature_unit": "celsius" if unit == "C" else "fahrenheit",
        },
        timeout=10,
    )
    resp.raise_for_status()
    current = resp.json()["current"]
    temp: float = current["temperature_2m"]
    desc = _WMO.get(current["weathercode"], "Unknown")
    return temp, desc


def _daemonize() -> None:
    pid = os.fork()
    if pid > 0:
        print(f"Weather daemon started (PID {pid})")
        os._exit(0)
    os.setsid()
    for fd, mode in [(0, "r"), (1, "w"), (2, "w")]:
        with open(os.devnull, mode) as f:
            os.dup2(f.fileno(), fd)


def main(host: str | None = None, args: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Weather app on AWTRIX.")
    parser.add_argument(
        "--location",
        default=os.environ.get("WEATHER_LOCATION", "San Jose"),
        help="Location name (default: San Jose or $WEATHER_LOCATION).",
    )
    parser.add_argument(
        "--unit",
        choices=["C", "F"],
        default=os.environ.get("WEATHER_UNIT", "C"),
        help="Temperature unit (default: C or $WEATHER_UNIT).",
    )
    parser.add_argument(
        "--daemon", action="store_true", help="Run in the background as a daemon."
    )
    parsed = parser.parse_args(args)

    if parsed.daemon:
        if not hasattr(os, "fork"):
            print("--daemon is not supported on this platform", file=sys.stderr)
            sys.exit(1)
        _daemonize()

    sdk = AwtrixSDK(host or os.environ["AWTRIX_HOST"])
    lat, lon = _geocode(parsed.location)

    stop = threading.Event()
    signal.signal(signal.SIGTERM, lambda *_: stop.set())

    try:
        first = True
        while not stop.is_set():
            temp, desc = _fetch(lat, lon, parsed.unit)
            sdk.create_app(
                "weather",
                text=f"{desc} {temp:.0f}°{parsed.unit}",
                color="#FF8000",
                duration=10,
                scroll_speed=50,
            )
            if first:
                sdk.switch_app("weather")
                first = False
            stop.wait(300)
    finally:
        sdk.delete_app("weather")


if __name__ == "__main__":
    main()
