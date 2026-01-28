from machine import Pin
from utime import ticks_ms, ticks_diff

class Button:
    def __init__(self, pin: int, pull_up: bool = True, debounce_ms: int = 50):
        """
        Button driver with optional pull-up/down and software debouncing.

        pin: GPIO pin number the button is connected to
        pull_up: True -> internal pull-up resistor, False -> pull-down
        debounce_ms: minimum stable time before a press is accepted
        """

        # Choose the correct internal resistor mode
        # Pull-up: default HIGH, button press pulls LOW
        # Pull-down: default LOW, button press pulls HIGH
        pull = Pin.PULL_UP if pull_up else Pin.PULL_DOWN

        self._pin = Pin(pin, Pin.IN, pull) # Create the GPIO input pin
        self._pull_up = pull_up
        self._debounce_ms = debounce_ms
        self._last_change = ticks_ms() # Time (ms) when the input last changed state
        self._last_state = self._pin.value() # Last raw pin value (0 or 1)

    def pressed(self) -> bool:
        """
        Immediate (non-debounced) button state.

        Returns True if the button is currently pressed.
        """
        level = self._pin.value()
        return (level == 0) if self._pull_up else (level == 1)

    def pressed_debounced(self) -> bool:
        """
        Debounced button press detection.

        Returns True only if the button has been held
        steadily for at least debounce_ms milliseconds.
        """
        now = ticks_ms()
        state = self._pin.value()

        # Detect any change in raw pin state
        if state != self._last_state:
            self._last_state = state
            self._last_change = now   # reset debounce timer

        # Check if the state has been stable long enough
        if ticks_diff(now, self._last_change) >= self._debounce_ms:
            # Apply pull-up / pull-down logic
            return (state == 0) if self._pull_up else (state == 1)
        
        # Not stable long enough → ignore
        return False