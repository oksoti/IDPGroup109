from utime import sleep_ms

from src.drivers.line_sensor import LineSensorArray
from src.drivers.motor import Motor, MotorPair
import src.config as config
from src.controllers.bay_controller import BayController
import random

# --- Motor pin configuration (UPDATE to match your wiring) ---
'''LEFT_MOTOR_DIR_PIN = 6
LEFT_MOTOR_PWM_PIN = 7
RIGHT_MOTOR_DIR_PIN = 8
RIGHT_MOTOR_PWM_PIN = 9'''

# --- Speeds ---
BASE_SPEED = 1.0
REALIGN_SPEED = 0.6

# --- Hardware init ---
line_sensor = LineSensorArray(config.LINE_PINS, white_is_1=config.LINE_WHITE_IS_1)

left_motor = Motor(config.LEFT_DIR_PIN, config.LEFT_PWM_PIN)
right_motor = Motor(config.RIGHT_DIR_PIN, config.RIGHT_PWM_PIN)
motors = MotorPair(left_motor, right_motor)

print("Running. Press Ctrl+C to stop.")

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







