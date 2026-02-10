from utime import sleep_ms
from machine import I2C, Pin

# Sensors
from libs.VL53L0X.VL53L0X import VL53L0X
from libs.DFRobot_TMF8x01.DFRobot_TMF8x01 import DFRobot_TMF8701

# Drivers
from src.drivers.line_sensor import LineSensorArray
from src.drivers.motor import Motor, MotorPair
from src.drivers.box_detector import BoxDetector
from src.drivers.button import Button
from src.drivers.led import LED
from src.controllers.navigator import Navigator
from src.controllers.rack_controller import RackController

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

left_detector = BoxDetector(
    left_tof,
    threshold_mm=config.BAY_OCCUPIED_THRESHOLD_MM_LEFT,
    samples=config.BOX_SAMPLES,
    sample_delay_ms=config.BOX_SAMPLE_DELAY_MS
)

right_detector = BoxDetector(
    right_tof,
    threshold_mm=config.BAY_OCCUPIED_THRESHOLD_MM_RIGHT,
    samples=config.BOX_SAMPLES,
    sample_delay_ms=config.BOX_SAMPLE_DELAY_MS
)

print("Running. Press Ctrl+C to stop.")

rack_controller = RackController(left_detector, right_detector)

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

print(rack_controller.rack_occupied(2))

navigator.leave_start_box()
navigator.go_to_pickup_bay(1)
navigator.go_to_rack(4)
for i in range(6):
    navigator.line_follow_until(0, 1)
    if rack_controller.rack_occupied(4):
        led_2.on()
        navigator.skip_junction(0, 1)
    else:
        led_3.on()
        navigator.approach_rack()
        navigator.exit_rack()
        break
navigator.return_to_start_line()
navigator.go_to_pickup_bay(0)
navigator.enter_start_box()
