from machine import Pin, PWM


class Motor:
    def __init__(self, dir_pin, pwm_pin, freq=1000):
        self.dir = Pin(dir_pin, Pin.OUT)
        self.pwm = PWM(Pin(pwm_pin))
        self.pwm.freq(freq)
        self.pwm.duty_u16(0)

    def set_speed(self, speed):
        if speed >= 0:
            self.dir.value(0)
        else:
            self.dir.value(1)
            speed = -speed
        self.pwm.duty_u16(int(min(speed, 1.0) * 65535))

    def off(self):
        self.pwm.duty_u16(0)


class MotorPair:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    @staticmethod
    def _clamp(x, lo, hi):
        return lo if x < lo else hi if x > hi else x

    def speeds_from_turn(self, turn, base=0.5, max_speed=1.0, min_speed=0.0):
        '''
        Convert a turn command into left/right motor speeds.

        Parameters:
        turn: float, typically in [-1, 1] (from your PD controller)
        base: float, forward speed baseline (0..1)
        max_speed: float, cap for motor command
        min_speed: float, minimum allowed (0 means don't reverse)

        Returns:
        (left, right) floats in [min_speed, max_speed]
        '''
        left = base - turn
        right = base + turn

        left = self._clamp(left, min_speed, max_speed)
        right = self._clamp(right, min_speed, max_speed)
        return left, right

    def drive(self, left_speed, right_speed):
        self.left.set_speed(left_speed)
        self.right.set_speed(right_speed)

    def stop(self):
        self.left.off()
        self.right.off()
