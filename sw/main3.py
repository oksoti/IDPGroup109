from utime import sleep_ms
from machine import I2C, Pin

# Sensors
from libs.VL53L0X.VL53L0X import VL53L0X
from libs.DFRobot_TMF8x01.DFRobot_TMF8x01 import DFRobot_TMF8701

# Drivers
from src.drivers.line_sensor import LineSensorArray
from src.drivers.motor import Motor, MotorPair
from src.drivers.box_detector import SideBoxDetector
from src.drivers.button import Button
from src.drivers.led import LED
from src.controllers.navigator import Navigator
from src.controllers.bay_controller import BayController

# Config
import src.config as config

# --- Motor pin configuration (UPDATE to match your wiring) ---
'''LEFT_MOTOR_DIR_PIN = 6
LEFT_MOTOR_PWM_PIN = 7
RIGHT_MOTOR_DIR_PIN = 8
RIGHT_MOTOR_PWM_PIN = 9'''

# --- Hardware init ---
line_sensor = LineSensorArray(config.LINE_PINS)

left_motor = Motor(config.LEFT_DIR_PIN, config.LEFT_PWM_PIN, speed_mult=0.95)
right_motor = Motor(config.RIGHT_DIR_PIN, config.RIGHT_PWM_PIN, speed_mult=1.0)
motors = MotorPair(left_motor, right_motor)

i2c_left = I2C(config.I2C_ID_left, scl=Pin(config.I2C_SCL_PIN_left), sda=Pin(config.I2C_SDA_PIN_left), freq=config.I2C_FREQ_left)
i2c_right = I2C(config.I2C_ID_right, scl=Pin(config.I2C_SCL_PIN_right), sda=Pin(config.I2C_SDA_PIN_right), freq=config.I2C_FREQ_right)

left_tof = VL53L0X(i2c_left)          # VL53 init
right_tof = DFRobot_TMF8701(i2c_right) # TMF init

left_detector = SideBoxDetector(
    left_tof,
    threshold_mm=config.BAY_OCCUPIED_THRESHOLD_MM_LEFT,
    samples=config.BOX_SAMPLES,
    sample_delay_ms=config.BOX_SAMPLE_DELAY_MS
)

right_detector = SideBoxDetector(
    right_tof,
    threshold_mm=config.BAY_OCCUPIED_THRESHOLD_MM_RIGHT,
    samples=config.BOX_SAMPLES,
    sample_delay_ms=config.BOX_SAMPLE_DELAY_MS
)

print("Running. Press Ctrl+C to stop.")

bay_controller = BayController(left_detector, right_detector)

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

print(bay_controller.bay_occupied(2))

navigator.leave_start_box()
navigator.go_to_pickup_bay(1)
navigator.go_to_rack(1)
for i in range(6):
    navigator.line_follow_until(0, 1)
    if bay_controller.bay_occupied(1):
        led_2.on()
        navigator.skip_junction(0, 1)
    else:
        led_3.on()
        break
navigator.turn_right()
motors.drive(config.BASE_SPEED, config.BASE_SPEED)
sleep_ms(int(250.0 / config.BASE_SPEED))
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
