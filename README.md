# awtctl

CLI and Python SDK for controlling [AWTRIX 3](https://blueforcer.github.io/awtrix3) LED matrix devices over HTTP.

## Installation

### pipx (recommended for CLI use)

```bash
pipx install git+https://github.com/happyslowly/awtctl.git
```

### pip

```bash
pip install git+https://github.com/happyslowly/awtctl.git
```

### From source

```bash
git clone https://github.com/happyslowly/awtctl.git
cd awtctl
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

### Built-in Apps

Run ready-to-use apps directly from the CLI:

```bash
awtctl run cpu
awtctl run weather
awtctl run pomodoro 25
awtctl run pomodoro --help
awtctl run fitness --rounds 8 --work 30 --rest 10 --prepare 10
awtctl run fitness --help
```

`weather` uses `WEATHER_LOCATION` (default `London`) and `WEATHER_UNIT` (`C`/`F`) env vars.

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
