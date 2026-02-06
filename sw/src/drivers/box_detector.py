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

        if hasattr(self.sensor, "begin"):
            while sensor.begin() != 0:
                sleep_ms(100)
            sensor.start_measurement(calib_m = sensor.eMODE_NO_CALIB, mode = sensor.eDISTANCE)
        else:
            sensor.set_Vcsel_pulse_period(sensor.vcsel_period_type[0], 18)
            sensor.set_Vcsel_pulse_period(sensor.vcsel_period_type[1], 14)
            sensor.start()

    def read_distance_mm(self):
        # VL53L0X library: .read()
        if hasattr(self.sensor, "read"):
            for _ in range(10):
                d = self.sensor.read()
                if d is not None and self.valid_min_mm <= d <= self.valid_max_mm:
                    return d
            return None
        # TMF8701 library: .get_distance_mm()
        if hasattr(self.sensor, "get_distance_mm"):
            while self.sensor.is_data_ready() == False:
                sleep_ms(10)
            for _ in range(10):
                d = self.sensor.get_distance_mm()
                if d is not None and self.valid_min_mm <= d <= self.valid_max_mm:
                    return d
                sleep_ms(10)
            return None
        raise RuntimeError("Sensor must provide read() or get_distance_mm()")

    def bay_occupied(self):
        close = 0
        valid = 0

        d = self.read_distance_mm()
        print(d)
        if d is not None:
            return d <= self.threshold_mm
        else:
            return False
