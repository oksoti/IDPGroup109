from machine import PWM, Pin

class Servo:
    def __init__(self, pin_number, freq=50):
        self.pwm = PWM(Pin(pin_number))
        self.pwm.freq(freq)

    def set_angle(self, angle):
        duty = int(1500 +(angle / 270) * 7000) # 1500 for 0 degrees, 8500 for 270 degrees
        self.pwm.duty_u16(duty)