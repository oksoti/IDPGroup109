from utime import sleep_ms
from machine import I2C, Pin

# Sensors
from libs.VL53L0X.VL53L0X import VL53L0X
from libs.DFRobot_TMF8x01.DFRobot_TMF8x01 import DFRobot_TMF8701

# Drivers
from src.drivers.line_sensor import LineSensorArray
from src.drivers.motor import Motor, MotorPair
from sw.src.drivers.distance_sensor import DistanceSensor
from src.drivers.button import Button
from src.drivers.led import LED, LEDPanel
from src.controllers.navigator import Navigator
from sw.src.controllers.box_detector import BoxDetector
from src.controllers.grabber import Grabber
from src.drivers.servo import Servo
from src.drivers.resistance_measurer import ResistanceMeasurer

# Config
import src.config as config

# --- Hardware init ---
line_sensor = LineSensorArray(config.LINE_PINS)

left_motor = Motor(config.LEFT_DIR_PIN, config.LEFT_PWM_PIN, speed_mult=0.95)
right_motor = Motor(config.RIGHT_DIR_PIN, config.RIGHT_PWM_PIN, speed_mult=1.0)
motors = MotorPair(left_motor, right_motor)

i2c_left = I2C(config.I2C_ID_left, scl=Pin(config.I2C_SCL_PIN_left), sda=Pin(config.I2C_SDA_PIN_left), freq=config.I2C_FREQ_left)
i2c_right = I2C(config.I2C_ID_right, scl=Pin(config.I2C_SCL_PIN_right), sda=Pin(config.I2C_SDA_PIN_right), freq=config.I2C_FREQ_right)

left_tof = VL53L0X(i2c_left)          # VL53 init
right_tof = DFRobot_TMF8701(i2c_right) # TMF init

left_sensor = DistanceSensor(
    left_tof,
    threshold_mm=config.BAY_OCCUPIED_THRESHOLD_MM_LEFT,
    samples=config.BOX_SAMPLES,
    sample_delay_ms=config.BOX_SAMPLE_DELAY_MS
)

right_sensor = DistanceSensor(
    right_tof,
    threshold_mm=config.BAY_OCCUPIED_THRESHOLD_MM_RIGHT,
    samples=config.BOX_SAMPLES,
    sample_delay_ms=config.BOX_SAMPLE_DELAY_MS
)

print("Running. Press Ctrl+C to stop.")

box_detector = BoxDetector(left_sensor, right_sensor)

# did_turn = bay_controller.attempt_turn_into_bay("left")

navigator = Navigator(motors, line_sensor)

# Grabber setup
tilt_servo = Servo(config.SERVO_1_PIN, config.SERVO_FREQ)
jaw_servo = Servo(config.SERVO_2_PIN, config.SERVO_FREQ)
grabber = Grabber(tilt_servo, jaw_servo)

button = Button(config.START_BUTTON_PIN)
led_1 = LED(config.LED_1_PIN)
led_2 = LED(config.LED_2_PIN)
led_3 = LED(config.LED_3_PIN)
led_4 = LED(config.LED_4_PIN)

led_panel = LEDPanel([led_1, led_2, led_3, led_4])

resistance_measurer = ResistanceMeasurer(config.ADC_PIN_NUMBER)

# simple loop to test the box detection before starting the main routine (waiting for the button to be pressed)
while not button.pressed():
    sleep_ms(10)

# Home the grabber before starting
grabber.home()

# Leave start box
navigator.leave_start_box()

for bay_number in range(1, 5):
    led_panel.all_off()
    
    # Go to pickup bay
    navigator.go_to_pickup_bay(bay_number)

    # Pick up box
    grabber.pick()

    rack_number = resistance_measurer.measure_resistance()

    led_panel.on(rack_number)

    # Go to rack
    navigator.go_to_rack(rack_number)

    # find an empty rack slot & place the box down
    for i in range(6):
        if rack_number == 1 or rack_number == 2:
            navigator.line_follow_until(0, 1)
        else:
            navigator.line_follow_until(1, 0)
        
        if box_detector.rack_occupied(rack_number):
            led_2.on()
            if rack_number == 1 or rack_number == 2:
                navigator.skip_junction(0, 1)
            else:
                navigator.skip_junction(1, 0)
        else:
            navigator.approach_rack()
            grabber.tilt_downwards()
            grabber.open_part()
            navigator.exit_rack()
            grabber.home()
            break

    navigator.return_to_start_line()

# Return to start box
navigator.go_to_pickup_bay(0)
navigator.enter_start_box()
