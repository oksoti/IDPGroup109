from machine import Pin, PWM
from utime import sleep_ms


class Motor: # class to control one of the motors
    def __init__(self, dir_pin, pwm_pin, freq=1000, speed_mult=1.0):
        self.dir = Pin(dir_pin, Pin.OUT)
        self.pwm = PWM(Pin(pwm_pin))
        self.pwm.freq(freq)
        self.pwm.duty_u16(0)
        self.speed_mult = speed_mult

    def set_speed(self, speed):
        speed *= self.speed_mult
        if speed >= 0:
            self.dir.value(0)
        else:
            self.dir.value(1)
            speed = -speed
        self.pwm.duty_u16(int(min(speed, 1.0) * 65535))

    def off(self):
        self.pwm.duty_u16(0)


class MotorPair: # class to control both motors
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def drive(self, left_speed, right_speed):
        self.left.set_speed(left_speed)
        self.right.set_speed(right_speed)

    def stop(self):
        self.left.off()
        self.right.off()
