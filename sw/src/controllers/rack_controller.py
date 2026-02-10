from utime import sleep_ms

class RackController:
    def __init__(self, left_detector, right_detector):
        self.left_detector = left_detector     # VL53L0X side
        self.right_detector = right_detector   # TMF8701 side

    def rack_occupied(self, rack_number):
        # Bays 1&3: check RIGHT sensor (TMF8701)
        if rack_number in (1, 3):
            return self.right_detector.bay_occupied()
        # Bays 2&4: check LEFT sensor (VL53L0X)
        if rack_number in (2, 4):
            return self.left_detector.bay_occupied()
        raise ValueError("bay_number must be 1, 2, 3, or 4")

