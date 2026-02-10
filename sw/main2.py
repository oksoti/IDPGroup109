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
from src.drivers.servo import Servo
from src.controllers.grabber import Grabber

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

tilt_servo = Servo(config.TILT_SERVO_PIN)
jaw_servo = Servo(config.JAW_SERVO_PIN)
grabber = Grabber(tilt_servo, jaw_servo)

grabber.home()

# did_turn = bay_controller.attempt_turn_into_bay("left")

navigator = Navigator(motors, line_sensor)

button = Button(config.START_BUTTON_PIN)
led_1 = LED(config.LED_1_PIN)
led_2 = LED(config.LED_2_PIN)
led_3 = LED(config.LED_3_PIN)
led_4 = LED(config.LED_4_PIN)


while not button.pressed():
    sleep_ms(100)

grabber.pick()

grabber.drop()

