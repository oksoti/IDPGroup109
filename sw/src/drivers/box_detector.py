from utime import sleep_ms

class BoxDetector:
    def __init__(self, sensor, threshold_mm=200, samples=7, settle_ms=10):
        """
        sensor: object with read() or get_distance_mm()
        threshold_mm: distance below which a box is considered present
        samples: number of samples for confirmation
        settle_ms: delay between samples
        """
        self.sensor = sensor
        self.threshold = threshold_mm
        self.samples = samples
        self.settle_ms = settle_ms

    def read_distance_mm(self):
        """
        Unify different sensor APIs into one call.
        """
        if hasattr(self.sensor, "read"):
            return self.sensor.read()
        elif hasattr(self.sensor, "get_distance_mm"):
            return self.sensor.get_distance_mm()
        else:
            raise RuntimeError("Unsupported distance sensor API")

    def object_confirmed(self):
        """
        Returns True if a box is detected within threshold distance.
        """
        close_count = 0

        for _ in range(self.samples):
            d = self.read_distance_mm()

            if d is not None and d > 0 and d <= self.threshold:
                close_count += 1

            sleep_ms(self.settle_ms)

        # Require majority agreement
        return close_count >= (self.samples // 2 + 1)
