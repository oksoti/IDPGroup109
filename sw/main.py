from utime import sleep_ms

from src.drivers.line_sensor import LineSensorArray
from src.drivers.motor import Motor, MotorPair
import src.config as config
from src.controllers.navigator import Navigator

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

navigator = Navigator(motors, line_sensor)

navigator.leave_start_box()
for i in range(1, 5):
    navigator.go_to_pickup_bay(i)
    navigator.go_to_rack(i)
    navigator.return_to_start_line()

# # leaving the start box
# motors.drive(BASE_SPEED, BASE_SPEED)
# while True:
#     ol, ml, mr, or_ = line_sensor.read_named()
#     if ol == 1 and or_ == 1:
#         sleep_ms(200)
#         break
#     sleep_ms(10)

'''line_follow_until(1, 1)
motors.turn_right(90)
skip_junction(0, 1)
line_follow_until(1, 1)
motors.turn_left(90)
skip_junction(1, 1)
line_follow_until(1, 0)
motors.turn_left(90)
skip_junction(1, 0)
line_follow_until(1, 0)
motors.turn_left(90)
skip_junction(1, 1)
skip_junction(1, 0, 6)
line_follow_until(1, 0)
motors.turn_left(90)
skip_junction(0, 1)
line_follow_until(0, 1)
motors.turn_right(90)
motors.drive(BASE_SPEED, BASE_SPEED)
sleep_ms(600)
motors.stop()'''

line_follow_until(0, 1)
motors.turn_right(90)
motors.drive(BASE_SPEED, BASE_SPEED)
sleep_ms(1000)
line_follow_until_rev(1,1)
