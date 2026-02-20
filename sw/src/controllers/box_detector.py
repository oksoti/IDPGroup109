class BoxDetector:
    def __init__(self, left_detector, right_detector):
        self.left_detector = left_detector
        self.right_detector = right_detector

    def rack_occupied(self, rack_number):
        # Bays 1&3: check RIGHT sensor
        if rack_number in (1, 3):
            return self.right_detector.rack_occupied()
        # Bays 2&4: check LEFT sensor (VL53L0X)
        if rack_number in (2, 4):
            return self.left_detector.rack_occupied()
        raise ValueError("rack_number must be 1, 2, 3, or 4")

