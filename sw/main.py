from utime import sleep_ms

from config import LEFT_PWM_PIN, RIGHT_PWM_PIN
from line_sensor import LineSensorArray
from motor import Motor, MotorPair
import config

# --- Motor pin configuration (UPDATE to match your wiring) ---
'''LEFT_MOTOR_DIR_PIN = 6
LEFT_MOTOR_PWM_PIN = 7
RIGHT_MOTOR_DIR_PIN = 8
RIGHT_MOTOR_PWM_PIN = 9'''

# --- Speeds ---
BASE_SPEED = 0.8
REALIGN_SPEED = 0.3

# --- Hardware init ---
line_sensor = LineSensorArray(config.LINE_PINS, white_is_1=config.LINE_WHITE_IS_1)

left_motor = Motor(config.LEFT_DIR_PIN, LEFT_PWM_PIN)
right_motor = Motor(config.RIGHT_DIR_PIN, RIGHT_PWM_PIN)
motors = MotorPair(left_motor, right_motor)

print("Running. Press Ctrl+C to stop.")

try:
    while True:
        ol, ml, mr, or_ = line_sensor.read_named()

        if ml == 1 and mr == 1 and ol == 1 and or_ == 1:
            # Left corner: outer-left + both middles see white
            motors.turn_left(90)
            motors.drive(BASE_SPEED, BASE_SPEED)
            sleep_ms(200)  # drive forward past the junction
        elif ml == 1 and mr == 1 and or_ == 1 and ol == 1:
            # Right corner: outer-right + both middles see white
            motors.turn_right(90)
            motors.drive(BASE_SPEED, BASE_SPEED)
            sleep_ms(200)  # drive forward past the junction
        elif ml == 1 and mr == 1 and or_ == 0 and ol == 0:
            # Aligned: both middles on the line
            motors.drive(BASE_SPEED, BASE_SPEED)
        elif ml == 1 and mr == 0 and ol == 1 and or_ == 0:
            # Drifted left of line: left-mid sees it but right-mid lost it -> turn right
            motors.drive(REALIGN_SPEED, BASE_SPEED)
        elif ml == 0 and mr == 1 and or_ == 1 and ol == 0:
            # Drifted right of line: right-mid sees it but left-mid lost it -> turn left
            motors.drive(BASE_SPEED, REALIGN_SPEED)
        else:
            # Line lost (0,0,0,0 or unexpected state): stop
            motors.stop()

        sleep_ms(10)
except KeyboardInterrupt:
    motors.stop()
    print("Stopped.")
