from machine import Pin

class Button:
    def __init__(self, pin):
        self._pin = Pin(pin, Pin.IN, Pin.PULL_DOWN)

    def pressed(self):
        level = self._pin.value()
        return level == 1
