from machine import PWM, Pin, ADC
from utime import sleep_ms

class Servo: # class to control one of the servos
    def __init__(self, pin_number, freq=50):
        self.pwm = PWM(Pin(pin_number))
        self.pwm.freq(freq)
        self.pwm.duty_u16(0)  # Start with the servo off

    def set_angle(self, current_angle, desired_angle): # move gradually from current_angle to desired_angle
        current_duty = int(1500 + (current_angle / 270) * 7000)  # 1500 for 0 degrees, 8500 for 270 degrees
        desired_duty = int(1500 + (desired_angle / 270) * 7000)  # 1500 for 0 degrees, 8500 for 270 degrees
        if (desired_angle > current_angle):  
            for duty in range(current_duty,desired_duty,20):
                
                self.pwm.duty_u16(duty)
                sleep_ms(10)

        if (desired_angle < current_angle):   
            for duty in range(current_duty,desired_duty,-20):
                self.pwm.duty_u16(duty)
                sleep_ms(10)

        self.pwm.duty_u16(desired_duty)  # set to the final desired position
        sleep_ms(100)
