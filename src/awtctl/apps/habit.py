import argparse
import json
import os
from datetime import date, timedelta
from pathlib import Path

from awtctl import AwtrixSDK

_DATA = Path.home() / ".awtctl" / "habit.json"
_DONE = "#00CC00"
_MISS = "#555555"
_DONE_SYM = "■"
_MISS_SYM = "□"

_GRID_COLS = 18
_GRID_ROWS = 5   # 18×5 = 90 days
_GRID_X = 1      # 1px left margin
_GRID_Y = 1      # 1px top margin: y=1..5


def _load() -> dict:
    if _DATA.exists():
        data = json.loads(_DATA.read_text())
        if isinstance(data, dict):
            return data
    return {}


def _save(data: dict) -> None:
    _DATA.parent.mkdir(parents=True, exist_ok=True)
    _DATA.write_text(json.dumps(data, indent=2))


def _window(data: dict) -> tuple[date, int]:
    stored_start = date.fromisoformat(data["start"])
    today = date.today()
    effective_start = max(stored_start, today - timedelta(days=_GRID_COLS * _GRID_ROWS - 1))
    return effective_start, _GRID_COLS * _GRID_ROWS


def _streaks(done: set[str], start: date, days: int) -> tuple[int, int]:
    today = date.today()

    current = 0
    d = min(today, start + timedelta(days=days - 1))
    if d == today and today.isoformat() not in done:
        d -= timedelta(days=1)
    while d >= start:
        if d.isoformat() in done:
            current += 1
            d -= timedelta(days=1)
        else:
            break

    longest, streak = 0, 0
    for i in range(days):
        day = start + timedelta(days=i)
        if day > today:
            break
        if day.isoformat() in done:
            streak += 1
            longest = max(longest, streak)
        else:
            streak = 0

    return current, longest


def _push(sdk: AwtrixSDK, data: dict) -> None:
    start, days = _window(data)
    done = set(data.get("done", []))
    current, _ = _streaks(done, start, days)
    draw = []

    draw.append({"df": [_GRID_X, _GRID_Y, _GRID_COLS, _GRID_ROWS, _MISS]})
    for i in range(days):
        if (start + timedelta(days=i)).isoformat() in done:
            col = i % _GRID_COLS
            row = i // _GRID_COLS
            draw.append({"dp": [_GRID_X + col, _GRID_Y + row, _DONE]})

    today = date.today()
    habit_start = date.fromisoformat(data["start"])
    strip_days = min((today - habit_start).days + 1, 30)
    draw.append({"df": [1, 7, 30, 1, "#000000"]})
    if strip_days > 0:
        draw.append({"df": [1, 7, strip_days, 1, _MISS]})
    for i in range(strip_days):
        if (today - timedelta(days=i)).isoformat() in done:
            draw.append({"dp": [1 + i, 7, _DONE]})

    streak_color = _DONE if current > 0 else _MISS
    text = str(current)
    x = 20 + (12 - len(text) * 4) // 2
    draw.append({"dt": [x, 1, text, streak_color]})

    sdk.create_app("habit", draw=draw, duration=15)
    sdk.switch_app("habit")


def _log(data: dict) -> None:
    start, days = _window(data)
    done = set(data.get("done", []))
    current, _ = _streaks(done, start, days)
    total = sum(1 for i in range(days) if (start + timedelta(days=i)).isoformat() in done)
    cells = [
        _DONE_SYM if (start + timedelta(days=i)).isoformat() in done else _MISS_SYM
        for i in range(days)
    ]
    print(f"Start: {data['start']}  Window: {start}  Days: {days}")
    print(f"Streak: {current}  Done: {total}/{days}")
    for r in range(_GRID_ROWS):
        print(" ".join(cells[r * _GRID_COLS:(r + 1) * _GRID_COLS]))


def main(host: str | None = None, args: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Habit tracker on AWTRIX.")
    parser.add_argument(
        "action", nargs="?", default="push",
        choices=["push", "done", "log", "clear"],
        help="Action: push (default), done, log, clear.",
    )
    parser.add_argument(
        "date", nargs="?", default=None,
        help="Date for 'done' in YYYY-MM-DD format (default: today).",
    )
    parser.add_argument("--start", default=None, help="Start date YYYY-MM-DD (default: today, only used on init).")
    parsed = parser.parse_args(args)

    if parsed.action == "clear":
        if _DATA.exists():
            _DATA.unlink()
            print("Cleared.")
        else:
            print("Nothing to clear.")
        return

    if parsed.action == "log":
        data = _load()
        if not data:
            print("No habit data. Run 'awtctl run habit' to initialize.")
            return
        _log(data)
        return

    data = _load()
    if not data:
        start_str = parsed.start or date.today().isoformat()
        data = {"start": start_str, "days": 96, "done": []}
        _save(data)
        print(f"Initialized: {data['days']} days from {data['start']}")

    if parsed.action == "done":
        key = parsed.date or date.today().isoformat()
        done = set(data.get("done", []))
        done.add(key)
        data["done"] = sorted(done)
        _save(data)
        print(f"{key}: done")

    sdk = AwtrixSDK(host or os.environ["AWTRIX_HOST"])
    _push(sdk, data)


if __name__ == "__main__":
    main()
