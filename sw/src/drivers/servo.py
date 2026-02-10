from machine import PWM, Pin, ADC
from time import sleep

class Servo:
    def __init__(self, pin_number, freq=50):
        self.pwm = PWM(Pin(pin_number))
        self.pwm.freq(freq)
        self.pwm.duty_u16(0)  # Start with the servo off
        sleep(0.1)  # Short delay to ensure the servo initializes

    def set_angle(self, angle):
        duty = int(1500 + (angle / 270) * 7000)  # 1500 for 0 degrees, 8500 for 270 degrees
        self.pwm.duty_u16(duty)
        while True:
            for duty in range(1500,8500,100):
                self.pwm.duty_u16(duty)
                #print(f"Raw Value: {raw_value}, Voltage: {voltage:.2f}V")
                print(f"Processing position: {duty}")
                sleep(0.02)
                
            for duty in range(8500,1500,-100):
                self.pwm.duty_u16(duty)
                #print(f"Raw Value: {raw_value}, Voltage: {voltage:.2f}V")
                print(f"Processing position: {duty}")
                sleep(0.02)


