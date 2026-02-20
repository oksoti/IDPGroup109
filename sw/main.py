# IMPORTS #
from utime import sleep_ms
import src.config as config # config file

# drivers
from src.drivers.line_sensor import LineSensorArray
from src.drivers.motor import Motor, MotorPair
from src.drivers.distance_sensor import DistanceSensor
from src.drivers.button import Button
from src.drivers.led import LED, LEDPanel
from src.drivers.servo import Servo
from src.drivers.resistance_measurer import ResistanceMeasurer

# controllers
from src.controllers.navigator import Navigator
from src.controllers.box_detector import BoxDetector
from src.controllers.grabber import Grabber

# SETUP #
# setup line sensors
line_sensor = LineSensorArray(config.LINE_PINS)

# setup motors
left_motor = Motor(config.LEFT_DIR_PIN, config.LEFT_PWM_PIN, speed_mult=1.0)
right_motor = Motor(config.RIGHT_DIR_PIN, config.RIGHT_PWM_PIN, speed_mult=1.0)
motors = MotorPair(left_motor, right_motor)

# setup distance sensors
left_sensor = DistanceSensor(
    config.I2C_ID_LEFT, 
    config.I2C_SCL_PIN_LEFT, 
    config.I2C_SDA_PIN_LEFT, 
    config.I2C_FREQ_LEFT,
    threshold_mm=config.BAY_OCCUPIED_THRESHOLD_MM,
)

right_sensor = DistanceSensor(
    config.I2C_ID_RIGHT, 
    config.I2C_SCL_PIN_RIGHT, 
    config.I2C_SDA_PIN_RIGHT, 
    config.I2C_FREQ_RIGHT,
    threshold_mm=config.BAY_OCCUPIED_THRESHOLD_MM,
)

box_detector = BoxDetector(left_sensor, right_sensor) # setup box detector
navigator = Navigator(motors, line_sensor) # setup navigator

# Grabber setup
tilt_servo = Servo(config.TILT_SERVO_PIN, config.SERVO_FREQ)
jaw_servo = Servo(config.JAW_SERVO_PIN, config.SERVO_FREQ)
grabber = Grabber(tilt_servo, jaw_servo)

button = Button(config.START_BUTTON_PIN) # setup button

# setup LEDs
led_1 = LED(config.LED_1_PIN)
led_2 = LED(config.LED_2_PIN)
led_3 = LED(config.LED_3_PIN)
led_4 = LED(config.LED_4_PIN)
led_panel = LEDPanel([led_1, led_2, led_3, led_4])

resistance_measurer = ResistanceMeasurer(config.ADC_PIN_NUMBER) # setup resistance measurer

grabber.home() # move the grabber into its home position

# MAIN PROGRAM #
# wait for the button to be pressed
while not button.pressed():
    sleep_ms(100)

navigator.leave_start_box() # leave the start box

# for each pickup bay
for bay_number in range(1, 5):
    led_panel.all_off() # turn off the LEDs

    # go to the pickup bay
    navigator.go_to_pickup_bay(bay_number)

    # pick up a cable reel
    grabber.open_full()
    grabber.tilt_downwards()
    navigator.approach_bay()
    grabber.close()
    grabber.tilt_upwards()

    sleep_ms(1000) # small wait to help the resistance measurer
    
    resistance_number = resistance_measurer.measure_resistance() # measure the resistance of the cable reel
    led_panel.on(resistance_number) # turn on the corresponding LED

    rack_number = [2, 1, 3, 4][resistance_number - 1] # determine the corresponding rack number

    # go to that rack
    navigator.go_to_rack(rack_number)

    # find the first empty rack slot of 6
    for i in range(6):
        # advance to the correct junction (racks 1 & 3 on the right, racks 2 & 4 on the left)
        if rack_number == 1 or rack_number == 3:
            navigator.line_follow_until(0, 1, config.BOX_DETECTING_SPEED)
        else:
            navigator.line_follow_until(1, 0, config.BOX_DETECTING_SPEED)
        
        # check if the rack is occupied
        if box_detector.rack_occupied(rack_number):
            if i < 5: # advance to the next rack slot (if there is one)
                if rack_number == 1 or rack_number == 3:
                    navigator.skip_junction(0, 1, 1, config.BOX_DETECTING_SPEED)
                else:
                    navigator.skip_junction(1, 0, 1, config.BOX_DETECTING_SPEED)
            else: # if we have gone past all 6 racks without detecting an empty slot, drop the box and reset the grabber
                grabber.open_part()
                grabber.home()
                if rack_number == 2 or rack_number == 3: # for the upper racks, turn around
                    navigator.turn_around(rack_number == 3)
        else: # empty rack -> drop off the box
            navigator.approach_rack()
            grabber.open_part()
            navigator.exit_rack()
            grabber.home()
            break

    navigator.return_to_start_line() # return to the start line ready for the next pickup

# return to the start box
navigator.go_to_pickup_bay(0)
navigator.enter_start_box()
