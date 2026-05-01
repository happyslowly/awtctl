from awtctl._client import AwtrixClient


class AwtrixSDK:
    def __init__(self, host: str, timeout: float = 10.0) -> None:
        self._client = AwtrixClient(host, timeout)

    # Stats

    def get_stats(self) -> dict:
        return self._client.get("stats")

    def get_effects(self) -> list:
        return self._client.get("effects")

    def get_transitions(self) -> list:
        return self._client.get("transitions")

    def get_loop(self) -> list:
        return self._client.get("loop")

    def get_screen(self) -> list[int]:
        return self._client.get("screen")

    # Notifications

    def notify(
        self,
        text: str | None = None,
        *,
        text_case: int | None = None,
        top_text: bool = False,
        text_offset: int | None = None,
        center: bool = True,
        color: str | None = None,
        gradient: list | None = None,
        blink_text: int | None = None,
        fade_text: int | None = None,
        background: str | None = None,
        rainbow: bool = False,
        icon: str | None = None,
        push_icon: int | None = None,
        repeat: int | None = None,
        duration: int | None = None,
        hold: bool = False,
        sound: str | None = None,
        rtttl: str | None = None,
        loop_sound: bool = False,
        bar: list[int] | None = None,
        line: list[int] | None = None,
        autoscale: bool = True,
        bar_bc: str | None = None,
        progress: int | None = None,
        progress_c: str | None = None,
        progress_bc: str | None = None,
        draw: list | None = None,
        stack: bool = True,
        wakeup: bool = False,
        scroll: bool = True,
        clients: list[str] | None = None,
        scroll_speed: int | None = None,
        effect: str | None = None,
        effect_settings: dict | None = None,
        overlay: str | None = None,
    ) -> None:
        payload: dict = {}
        if text is not None: payload["text"] = text
        if text_case is not None: payload["textCase"] = text_case
        if top_text: payload["topText"] = True
        if text_offset is not None: payload["textOffset"] = text_offset
        if not center: payload["center"] = False
        if color: payload["color"] = color
        if gradient: payload["gradient"] = gradient
        if blink_text is not None: payload["blinkText"] = blink_text
        if fade_text is not None: payload["fadeText"] = fade_text
        if background: payload["background"] = background
        if rainbow: payload["rainbow"] = True
        if icon: payload["icon"] = icon
        if push_icon is not None: payload["pushIcon"] = push_icon
        if repeat is not None: payload["repeat"] = repeat
        if duration is not None: payload["duration"] = duration
        if hold: payload["hold"] = True
        if sound: payload["sound"] = sound
        if rtttl: payload["rtttl"] = rtttl
        if loop_sound: payload["loopSound"] = True
        if bar: payload["bar"] = bar
        if line: payload["line"] = line
        if not autoscale: payload["autoscale"] = False
        if bar_bc: payload["barBC"] = bar_bc
        if progress is not None: payload["progress"] = progress
        if progress_c: payload["progressC"] = progress_c
        if progress_bc: payload["progressBC"] = progress_bc
        if draw: payload["draw"] = draw
        if not stack: payload["stack"] = False
        if wakeup: payload["wakeup"] = True
        if not scroll: payload["noScroll"] = True
        if clients: payload["clients"] = clients
        if scroll_speed is not None: payload["scrollSpeed"] = scroll_speed
        if effect: payload["effect"] = effect
        if effect_settings: payload["effectSettings"] = effect_settings
        if overlay: payload["overlay"] = overlay
        self._client.post("notify", payload)

    def dismiss_notification(self) -> None:
        self._client.post("notify/dismiss", {})

    # Apps

    def create_app(
        self,
        name: str,
        text: str | None = None,
        *,
        text_case: int | None = None,
        top_text: bool = False,
        text_offset: int | None = None,
        center: bool = True,
        color: str | None = None,
        gradient: list | None = None,
        blink_text: int | None = None,
        fade_text: int | None = None,
        background: str | None = None,
        rainbow: bool = False,
        icon: str | None = None,
        push_icon: int | None = None,
        repeat: int | None = None,
        duration: int | None = None,
        bar: list[int] | None = None,
        line: list[int] | None = None,
        autoscale: bool = True,
        bar_bc: str | None = None,
        progress: int | None = None,
        progress_c: str | None = None,
        progress_bc: str | None = None,
        draw: list | None = None,
        pos: int | None = None,
        lifetime: int | None = None,
        lifetime_mode: int | None = None,
        scroll: bool = True,
        scroll_speed: int | None = None,
        effect: str | None = None,
        effect_settings: dict | None = None,
        overlay: str | None = None,
        save: bool = False,
    ) -> None:
        payload: dict = {}
        if text is not None: payload["text"] = text
        if text_case is not None: payload["textCase"] = text_case
        if top_text: payload["topText"] = True
        if text_offset is not None: payload["textOffset"] = text_offset
        if not center: payload["center"] = False
        if color: payload["color"] = color
        if gradient: payload["gradient"] = gradient
        if blink_text is not None: payload["blinkText"] = blink_text
        if fade_text is not None: payload["fadeText"] = fade_text
        if background: payload["background"] = background
        if rainbow: payload["rainbow"] = True
        if icon: payload["icon"] = icon
        if push_icon is not None: payload["pushIcon"] = push_icon
        if repeat is not None: payload["repeat"] = repeat
        if duration is not None: payload["duration"] = duration
        if bar: payload["bar"] = bar
        if line: payload["line"] = line
        if not autoscale: payload["autoscale"] = False
        if bar_bc: payload["barBC"] = bar_bc
        if progress is not None: payload["progress"] = progress
        if progress_c: payload["progressC"] = progress_c
        if progress_bc: payload["progressBC"] = progress_bc
        if draw: payload["draw"] = draw
        if pos is not None: payload["pos"] = pos
        if lifetime is not None: payload["lifetime"] = lifetime
        if lifetime_mode is not None: payload["lifetimeMode"] = lifetime_mode
        if not scroll: payload["noScroll"] = True
        if scroll_speed is not None: payload["scrollSpeed"] = scroll_speed
        if effect: payload["effect"] = effect
        if effect_settings: payload["effectSettings"] = effect_settings
        if overlay: payload["overlay"] = overlay
        if save: payload["save"] = True
        self._client.post(f"custom?name={name}", payload)

    def create_app_raw(self, name: str, payload: dict) -> None:
        self._client.post(f"custom?name={name}", payload)

    def delete_app(self, name: str) -> None:
        self._client.post(f"custom?name={name}", {})

    def switch_app(self, name: str) -> None:
        self._client.post("switch", {"name": name})

    def next_app(self) -> None:
        self._client.post("nextapp", {})

    def prev_app(self) -> None:
        self._client.post("previousapp", {})

    # Device

    def set_power(self, on: bool) -> None:
        self._client.post("power", {"power": on})

    def sleep(self, seconds: int) -> None:
        self._client.post("sleep", {"sleep": seconds})

    def reboot(self) -> None:
        self._client.post("reboot", {})

    def update_firmware(self) -> None:
        self._client.post("doupdate", {})

    # Settings

    def get_settings(self) -> dict:
        return self._client.get("settings")

    def update_settings(self, **kwargs) -> None:
        self._client.post("settings", {k.upper(): v for k, v in kwargs.items()})

    def reset_settings(self) -> None:
        self._client.post("resetSettings", {})
