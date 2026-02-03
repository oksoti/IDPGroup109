from machine import Pin, PWM
from utime import sleep_ms


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

    def drive(self, left_speed, right_speed):
        self.left.set_speed(left_speed)
        self.right.set_speed(right_speed)

    def turn_left(self, angle, turn_speed=1.0, ms_per_deg=10):
        duration = int(angle * ms_per_deg)
        self.left.set_speed(-0.3 * turn_speed)
        self.right.set_speed(turn_speed)
        sleep_ms(duration)
        self.stop()

    def turn_right(self, angle, turn_speed=1.0, ms_per_deg=10):
        duration = int(angle * ms_per_deg)
        self.left.set_speed(turn_speed)
        self.right.set_speed(-0.3 * turn_speed)
        sleep_ms(duration)
        self.stop()

    def stop(self):
        self.left.off()
        self.right.off()
