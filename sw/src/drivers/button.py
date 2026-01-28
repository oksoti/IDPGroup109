from machine import Pin
from utime import ticks_ms, ticks_diff

class Button:
    def __init__(self, pin: int, pull_up: bool = True, debounce_ms: int = 50):
        pull = Pin.PULL_UP if pull_up else Pin.PULL_DOWN
        self._pin = Pin(pin, Pin.IN, pull)
        self._pull_up = pull_up
        self._debounce_ms = debounce_ms
        self._last_change = ticks_ms()
        self._last_state = self._pin.value()

    def pressed(self) -> bool:
        level = self._pin.value()
        return (level == 0) if self._pull_up else (level == 1)

    def pressed_debounced(self) -> bool:
        now = ticks_ms()
        state = self._pin.value()

        if state != self._last_state:
            self._last_state = state
            self._last_change = now

        if ticks_diff(now, self._last_change) >= self._debounce_ms:
            return (state == 0) if self._pull_up else (state == 1)

        return False