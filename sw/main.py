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
from src.controllers.grabber import Grabber
from src.drivers.servo import Servo

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

bay_controller = RackController(left_detector, right_detector)

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

# simple loop to test the box detection before starting the main routine (waiting for the button to be pressed)
while not button.pressed():
    if bay_controller.rack_occupied(1):
        led_2.on()
        led_3.off()
    else:
        led_3.on()
        led_2.off()
    if bay_controller.rack_occupied(2):
        led_1.on()
        led_4.off()
    else:
        led_4.on()
        led_1.off()
    sleep_ms(1000)

led_1.on()
led_2.on()
led_3.on()
led_4.on()
sleep_ms(1000)
led_1.off()
led_2.off()
led_3.off()
led_4.off()

# Home the grabber before starting
grabber.home()

# Leave start box
navigator.leave_start_box()

# === Bay 1 -> Rack 1 ===
navigator.go_to_pickup_bay(1)
grabber.pick()
navigator.go_to_rack(1)
navigator.approach_rack()
grabber.drop()
navigator.exit_rack()
navigator.return_to_start_line()

# === Bay 2 -> Rack 2 ===
navigator.go_to_pickup_bay(2)
grabber.pick()
navigator.go_to_rack(2)
navigator.approach_rack()
grabber.drop()
navigator.exit_rack()
navigator.return_to_start_line()

# === Bay 3 -> Rack 3 ===
navigator.go_to_pickup_bay(3)
grabber.pick()
navigator.go_to_rack(3)
navigator.approach_rack()
grabber.drop()
navigator.exit_rack()
navigator.return_to_start_line()

# === Bay 4 -> Rack 4 ===
navigator.go_to_pickup_bay(4)
grabber.pick()
navigator.go_to_rack(4)
navigator.approach_rack()
grabber.drop()
navigator.exit_rack()
navigator.return_to_start_line()

# Return to start box
navigator.go_to_pickup_bay(0)
navigator.enter_start_box()
