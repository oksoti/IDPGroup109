from utime import sleep_ms
from machine import I2C, Pin
import random

# Sensors
from libs.VL53L0X.VL53L0X import VL53L0X
from libs.DFRobot_TMF8x01.DFRobot_TMF8x01 import DFRobot_TMF8701

# Drivers
from src.drivers.line_sensor import LineSensorArray
from src.drivers.motor import Motor, MotorPair
from src.drivers.box_detector import SideBoxDetector

# Controllers
from src.controllers.bay_controller import BayController

# Config
import src.config as config

# --- Speeds ---
BASE_SPEED = 1.0
REALIGN_SPEED = 0.6

# --- Hardware init ---
line_sensor = LineSensorArray(config.LINE_PINS, white_is_1=config.LINE_WHITE_IS_1)

left_motor = Motor(config.LEFT_DIR_PIN, config.LEFT_PWM_PIN)
right_motor = Motor(config.RIGHT_DIR_PIN, config.RIGHT_PWM_PIN)
motors = MotorPair(left_motor, right_motor)

print("Running. Press Ctrl+C to stop.")

i2c_left = I2C(config.I2C_ID_left, scl=Pin(config.I2C_SCL_PIN_left), sda=Pin(config.I2C_SDA_PIN_left), freq=config.I2C_FREQ_left)
i2c_right = I2C(config.I2C_ID_right, scl=Pin(config.I2C_SCL_PIN_right), sda=Pin(config.I2C_SDA_PIN_right), freq=config.I2C_FREQ_right)

left_tof = VL53L0X(i2c_left)          # VL53 init
right_tof = DFRobot_TMF8701(i2c_right) # TMF init

left_detector = SideBoxDetector(
    left_tof,
    threshold_mm=config.BAY_OCCUPIED_THRESHOLD_MM,
    samples=config.BOX_SAMPLES,
    sample_delay_ms=config.BOX_SAMPLE_DELAY_MS
)

right_detector = SideBoxDetector(
    right_tof,
    threshold_mm=config.BAY_OCCUPIED_THRESHOLD_MM,
    samples=config.BOX_SAMPLES,
    sample_delay_ms=config.BOX_SAMPLE_DELAY_MS
)

# bay_controller = BayController(drivetrain, box_detector, config)

# did_turn = bay_controller.attempt_turn_into_bay("left")

def line_follow_until(ol_target, or_target):
    while True:
        ol, ml, mr, or_ = line_sensor.read_named()

        if ol == ol_target and or_ == or_target:
            motors.stop()
            break

        if ml == 1 and mr == 1:
            motors.drive(BASE_SPEED, BASE_SPEED)
        elif ml == 1 and mr == 0:
            motors.drive(REALIGN_SPEED, BASE_SPEED)
        elif ml == 0 and mr == 1:
            motors.drive(BASE_SPEED, REALIGN_SPEED)
        else:
            motors.stop()

        sleep_ms(10)

def skip_junction(ol_target, or_target, quantity=1):
    for _ in range(quantity):
        line_follow_until(ol_target, or_target)
        motors.drive(BASE_SPEED, BASE_SPEED)
        sleep_ms(200)  # drive forward past the junction
        motors.stop()

def bring_to_bay1():
    line_follow_until(1,1)
    motors.turn_left(90)
    line_follow_until(1,1)
    motors.turn_right(90)
    line_follow_until(0,1)
    
def bring_to_middle_bay(bay_number):
    line_follow_until(1, 1)
    motors.turn_left(90)
    line_follow_until(1, 1)
    motors.turn_right(90)
    line_follow_until(1, 1)
    line_follow_until(0, 1)
    motors.turn_right(90)
    line_follow_until(0,1)
    motors.turn_right(90)
    line_follow_until(1,1)
    if bay_number == 2:
        motors.turn_right(90)
        line_follow_until(0,1)
        motors.turn_right(90)
    elif bay_number == 3:
        motors.turn_left(90)
        line_follow_until(1, 0)
        motors.turn_left(90)

def bring_to_bay4():
    line_follow_until(1, 1)
    motors.turn_right(90)
    line_follow_until(1, 1)
    motors.turn_left(90)
    line_follow_until(1, 0)

def test_target():
    return random.choice([1,2,3,4])

def grab_target(number):
    if number == 0:
        motors.turn_left(90)
        line_follow_until(1, 1)
        sleep_ms(200)
        motors.turn_around()
    elif number == 1:
        motors.turn_right(90)
        line_follow_until(1, 1)
        sleep_ms(200)
        motors.turn_around()

# leaving the start box
motors.drive(BASE_SPEED, BASE_SPEED)
while True:
    ol, ml, mr, or_ = line_sensor.read_named()
    if ol == 1 and or_ == 1:
        sleep_ms(200)
        break
    sleep_ms(10)

line_follow_until(1,1)
motors.turn_left(90)
line_follow_until(1,0)
grab_target(0)
bring_to_bay1()
'''bay = test_target()
if bay == 1:
    bring_to_bay1()
elif bay == 4:
    bring_to_bay4()
elif bay == 2:
    bring_to_middle_bay(2)
elif bay == 3:
    bring_to_middle_bay(3)'''







