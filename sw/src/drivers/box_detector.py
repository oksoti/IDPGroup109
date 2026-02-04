from utime import sleep_ms

class SideBoxDetector:
    """
    Generic occupancy detector for one distance sensor.
    Returns True if an object is detected within threshold_mm (e.g. 180mm).
    Uses multiple samples + majority vote to reduce noise.
    """

    def __init__(self, sensor, threshold_mm=180, samples=7, sample_delay_ms=10,
                 valid_min_mm=20, valid_max_mm=2000):
        self.sensor = sensor
        self.threshold_mm = threshold_mm
        self.samples = samples
        self.sample_delay_ms = sample_delay_ms
        self.valid_min_mm = valid_min_mm
        self.valid_max_mm = valid_max_mm

    def read_distance_mm(self):
        # VL53L0X library: .read()
        if hasattr(self.sensor, "read"):
            return self.sensor.read()
        # TMF8701 library: .get_distance_mm()
        if hasattr(self.sensor, "get_distance_mm"):
            return self.sensor.get_distance_mm()
        raise RuntimeError("Sensor must provide read() or get_distance_mm()")

    def bay_occupied(self):
        close = 0
        valid = 0

        for _ in range(self.samples):
            d = self.read_distance_mm()

            if d is not None and self.valid_min_mm <= d <= self.valid_max_mm:
                valid += 1
                if d <= self.threshold_mm:
                    close += 1

            sleep_ms(self.sample_delay_ms)

        # If too few valid readings (less than half of samples, or less than 3), treat as empty (or flip to True for fail-safe)
        if valid < max(3, self.samples // 2):
            return False
        
        # If majority of valid readings (greater than half of valid readings) are recorded as close, bay is occupied, and will return True
        return close >= (valid // 2 + 1)
