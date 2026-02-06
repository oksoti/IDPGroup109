#Import the PWM class from the machine module of MicroPython.
#In order to create a PWM pin to read input/output GPIOs, we will also import the PWM class. We will import the machine module that contains classes to interact with the GPIOs.
#The sleep module is also imported for use in delays.

from time import sleep
from machine import Pin, PWM, ADC

#Create a PWM pin object called ‘pwm’ to pass the pwm pin as a parameter. The parameter shows where the pin is connected in our case GP0.

pwm = PWM(Pin(13))

#Set up the frequency of the PWM signal.

pwm.freq(50)

#Start: This shows the starting value for the duty cycle. In our case, we start with position 1500 (corresponds to approx. 0 degree) in the first loop and position 8500 (corresponds to approx. 270 degree) in the 2 second for loop.
#Stop: This shows the stopping value for the duty cycle range. In our case, we stop at position 8500 (corresponds to approx. 270 degree) in the first loop and position 1500 (corresponds to approx. 0 degree) in the 2 second for loop.
#Step: This shows the incrementation value. We are incrementing by 50 in the first loop and -50 in the second loop. This will determine the speed of the rotation.
#range(start, stop, step).



while True:
    pwm.duty_u16(8500)
    
    sleep(2)
    
    pwm.duty_u16(1500)
    
    sleep(2)
    
    for position in range(1500,8500,100):
        pwm.duty_u16(position)
        #print(f"Raw Value: {raw_value}, Voltage: {voltage:.2f}V")
        print(f"Processing position: {position}")
        sleep(0.02)
        
    for position in range(8500,1500,-100):
        pwm.duty_u16(position)
        #print(f"Raw Value: {raw_value}, Voltage: {voltage:.2f}V")
        print(f"Processing position: {position}")
        sleep(0.02)