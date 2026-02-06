from utime import sleep_ms

from src.drivers.line_sensor import LineSensorArray
from src.drivers.motor import Motor, MotorPair
from src.drivers.button import Button
from src.drivers.led import LED
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

button = Button(config.START_BUTTON_PIN)
led_1 = LED(config.LED_1_PIN)
led_2 = LED(config.LED_2_PIN)
led_3 = LED(config.LED_3_PIN)
led_4 = LED(config.LED_4_PIN)


while not button.pressed():
    sleep_ms(100)

led_1.on()
led_2.on()
led_3.on()
led_4.on()
sleep_ms(1000)
led_1.off()
led_2.off()
led_3.off()
led_4.off()

# navigator.line_follow_until(1, 1)
# navigator.turn_left()
# navigator.line_follow_until(1, 1)

navigator.leave_start_box()
navigator.go_to_pickup_bay(1)
navigator.go_to_rack(1)
navigator.skip_junction(0, 1)
print('skipped')
navigator.line_follow_until(0, 1)
navigator.turn_right()
motors.drive(BASE_SPEED, BASE_SPEED)
sleep_ms(int(250.0 / BASE_SPEED))
navigator.line_follow_until(1, 1, True)
navigator.turn_left()
navigator.return_to_start_line()
navigator.go_to_pickup_bay(0)
navigator.enter_start_box()

# line following test:
# navigator.line_follow_until(1, 1)
# motors.turn_right(90)
# navigator.skip_junction(0, 1)
# navigator.line_follow_until(1, 1)
# motors.turn_left(90)
# navigator.skip_junction(1, 1)
# navigator.line_follow_until(1, 0)
# motors.turn_left(90)
# navigator.skip_junction(1, 0)
# navigator.line_follow_until(1, 0)
# motors.turn_left(90)
# navigator.skip_junction(1, 1)
# navigator.skip_junction(1, 0, 6)
# navigator.line_follow_until(1, 0)
# motors.turn_left(90)
# navigator.skip_junction(0, 1)
# navigator.line_follow_until(0, 1)
# motors.turn_right(90)
# motors.drive(BASE_SPEED, BASE_SPEED)
# sleep_ms(int(600.0 / BASE_SPEED))
# motors.stop()
