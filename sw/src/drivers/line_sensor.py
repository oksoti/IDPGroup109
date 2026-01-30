from machine import Pin


class LineSensorArray:
    """
    4 digital line sensors, ordered left->right:
    [outer_left, mid_left, mid_right, outer_right]
    Returns 1 for white (line), 0 for black (floor).
    """

    def __init__(self, pins, white_is_1=True):
        self.sensors = [Pin(p, Pin.IN) for p in pins]
        self.white_is_1 = white_is_1

    def read_raw(self):
        return [s.value() for s in self.sensors]

    def read(self):
        raw = self.read_raw()
        if self.white_is_1:
            return [int(v == 1) for v in raw]
        else:
            return [int(v == 0) for v in raw]

    def read_named(self):
        vals = self.read()
        return vals[0], vals[1], vals[2], vals[3]  # OL, ML, MR, OR
