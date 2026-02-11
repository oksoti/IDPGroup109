from machine import Pin

class LED:
    def __init__(self, pin):
        self.pin = Pin(pin, Pin.OUT)

    def on(self):
        self.pin.value(1)

    def off(self):
        self.pin.value(0)

    def toggle(self):
        self.pin.value(not self.pin.value())

class LEDPanel:
    def __init__(self, leds):
        self.leds = leds

    def all_on(self):
        for led in self.leds:
            led.on()

    def all_off(self):
        for led in self.leds:
            led.off()

    def on(self, num):
        self.leds[num + 1].on()