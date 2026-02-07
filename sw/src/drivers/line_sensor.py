from machine import Pin

class LineSensorArray:
    def __init__(self, pins):
        self.sensors = [Pin(p, Pin.IN) for p in pins]

    def read_raw(self):
        return [s.value() for s in self.sensors]

    def read(self):
        raw = self.read_raw()
        return [int(v == 1) for v in raw]

    def read_named(self):
        vals = self.read()
        return vals[0], vals[1], vals[2], vals[3]  # OL, ML, MR, OR
