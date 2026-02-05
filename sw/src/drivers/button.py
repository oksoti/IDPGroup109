from machine import Pin
from utime import ticks_ms

class Button:
    def __init__(self, pin: int):
        self._pin = Pin(pin, Pin.IN, Pin.PULL_DOWN) # Create the GPIO input pin

    def pressed(self) -> bool:
        level = self._pin.value()
        return level == 1
