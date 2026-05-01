# awtctl

CLI and Python SDK for controlling [AWTRIX 3](https://blueforcer.github.io/awtrix3) LED matrix devices over HTTP.

## Installation

```bash
uv sync
```

## Configuration

Set your device IP via environment variable or `--host` flag:

```bash
export AWTRIX_HOST=192.168.1.x
```

## CLI Usage

```bash
awtctl --help
```

### Stats

```bash
awtctl stats                  # device stats
awtctl stats effects          # list effects
awtctl stats transitions      # list transitions
awtctl stats loop             # list apps in loop
awtctl screen                 # render matrix in terminal
```

### Notifications

```bash
awtctl send "Hello!"
awtctl send "Alert" --color "#FF0000" --duration 10 --hold
awtctl dismiss
```

### Custom Apps

```bash
awtctl create my-app app.json
awtctl create my-app app.yaml
```

Example `app.json`:
```json
{
  "text": "CPU 42%",
  "color": "#FF8000",
  "progress": 42,
  "progressC": "#FF8000",
  "progressBC": "#1A1A1A"
}
```

### App Navigation

```bash
awtctl next
awtctl prev
awtctl switch Time
```

### Device Control

```bash
awtctl power on
awtctl power off
awtctl sleep 3600
awtctl reboot
awtctl update
```

### Configuration

```bash
awtctl config get
awtctl config set BRI=128 TCOL="#FF8000"
awtctl config reset
```

## SDK Usage

```python
from awtctl import AwtrixSDK

sdk = AwtrixSDK("192.168.1.x")

sdk.notify("Hello!", color="#FF8000", duration=10)
sdk.create_app("cpu", text="CPU 42%", progress=42, progress_c="#FF8000")
sdk.switch_app("Time")
sdk.set_power(True)
sdk.update_settings(bri=128, tcol="#FF8000")
stats = sdk.get_stats()
```

## Built-in Apps

Ready-to-run apps in `src/awtctl/apps/`:

### CPU Monitor

Displays local CPU usage with a progress bar, updated every 6 seconds.

```bash
uv run python src/awtctl/apps/cpu.py
```

### Weather

Displays current weather from [wttr.in](https://wttr.in), updated every 5 minutes.

```bash
WEATHER_LOCATION="New York" uv run python src/awtctl/apps/weather.py
WEATHER_LOCATION="Tokyo" WEATHER_UNIT="F" uv run python src/awtctl/apps/weather.py
```

### Pomodoro Timer

Countdown timer that locks the display for the duration. Sends a notification when done.

```bash
uv run python src/awtctl/apps/pomodoro.py        # 25 minutes
uv run python src/awtctl/apps/pomodoro.py 5      # 5 minutes
```
