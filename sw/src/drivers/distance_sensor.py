from machine import I2C, Pin
from libs.VL53L0X.VL53L0X import VL53L0X

class DistanceSensor:
    def __init__(self, id_, scl_pin, sda_pin, freq, threshold_mm=180, valid_min_mm=20):
        i2c = I2C(id_, scl=Pin(scl_pin), sda=Pin(sda_pin), freq=freq)
        self.sensor = VL53L0X(i2c)
        self.threshold_mm = threshold_mm
        self.valid_min_mm = valid_min_mm
        self.sensor.set_Vcsel_pulse_period(self.sensor.vcsel_period_type[0], 18)
        self.sensor.set_Vcsel_pulse_period(self.sensor.vcsel_period_type[1], 14)
        self.sensor.start()

    def read_distance_mm(self):
        # VL53L0X library: .read()
        for _ in range(10):
            d = self.sensor.read()
            if d is not None and self.valid_min_mm <= d:
                return d
        return None

    def rack_occupied(self):
        d = self.read_distance_mm()
        print(d)
        if d is not None:
            return d <= self.threshold_mm
        else:
            return False
