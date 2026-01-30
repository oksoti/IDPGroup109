from utime import sleep_ms
from sw.src.drivers.line_sensor import LineSensorArray
from sw.src.drivers.motor import Motor, MotorPair
from sw.src.controllers.line_controller import PDLineController
from sw.src import config



# --- Motor pin configuration (UPDATE to match your wiring) ---
LEFT_MOTOR_DIR_PIN = 6
LEFT_MOTOR_PWM_PIN = 7
RIGHT_MOTOR_DIR_PIN = 8
RIGHT_MOTOR_PWM_PIN = 9

# --- PD controller tuning ---
KP = 0.3
KD = 0.05
BASE_SPEED = 0.55


line_sensor = LineSensorArray(config.LINE_PINS, white_is_1=config.LINE_WHITE_IS_1)

left_motor = Motor(LEFT_MOTOR_DIR_PIN, LEFT_MOTOR_PWM_PIN)
right_motor = Motor(RIGHT_MOTOR_DIR_PIN, RIGHT_MOTOR_PWM_PIN)
motors = MotorPair(left_motor, right_motor)

controller = PDLineController(KP, KD)

print("Running. Press Ctrl+C to stop.")

try:
    while True:
        error = line_sensor.line_error()
        turn = controller.update(error)
        left, right = motors.speeds_from_turn(turn, base=BASE_SPEED)
        motors.drive(left, right)
        sleep_ms(10)
except KeyboardInterrupt:
    motors.stop()
    print("Stopped.")
