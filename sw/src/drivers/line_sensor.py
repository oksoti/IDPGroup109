from machine import Pin

class LineSensorArray:
    def __init__(self, pins, white_is_1=True):
        self.sensors = [Pin(p, Pin.IN) for p in pins]
        self.white_is_1 = white_is_1
        self.weights = [-3, -1, 1, 3]

    def read_raw(self):
        return [s.value() for s in self.sensors]

    def read_white(self):
        raw = self.read_raw()
        if self.white_is_1:
            return [1 if v == 1 else 0 for v in raw]
        else:
            return [1 if v == 0 else 0 for v in raw]

    def line_error(self):
        whites = self.read_white()
        total = sum(whites)
        if total == 0:
            return None  # line lost
        weighted = sum(w * wht for w, wht in zip(self.weights, whites))
        return weighted / total