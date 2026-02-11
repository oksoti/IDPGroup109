from utime import sleep_ms

# Drivers
from src.drivers.line_sensor import LineSensorArray
from src.drivers.motor import Motor, MotorPair
from src.drivers.distance_sensor import DistanceSensor
from src.drivers.button import Button
from src.drivers.led import LED, LEDPanel
from src.controllers.navigator import Navigator
from src.controllers.box_detector import BoxDetector
from src.controllers.grabber import Grabber
from src.drivers.servo import Servo
from src.drivers.resistance_measurer import ResistanceMeasurer

# Config
import src.config as config

# --- Hardware init ---
line_sensor = LineSensorArray(config.LINE_PINS)

left_motor = Motor(config.LEFT_DIR_PIN, config.LEFT_PWM_PIN, speed_mult=1.0)
right_motor = Motor(config.RIGHT_DIR_PIN, config.RIGHT_PWM_PIN, speed_mult=1.0)
motors = MotorPair(left_motor, right_motor)

left_sensor = DistanceSensor(
    config.I2C_ID_LEFT, 
    config.I2C_SCL_PIN_LEFT, 
    config.I2C_SDA_PIN_LEFT, 
    config.I2C_FREQ_LEFT,
    threshold_mm=config.BAY_OCCUPIED_THRESHOLD_MM,
)

right_sensor = DistanceSensor(
    config.I2C_ID_RIGHT, 
    config.I2C_SCL_PIN_RIGHT, 
    config.I2C_SDA_PIN_RIGHT, 
    config.I2C_FREQ_RIGHT,
    threshold_mm=config.BAY_OCCUPIED_THRESHOLD_MM,
)

print("Running. Press Ctrl+C to stop.")

box_detector = BoxDetector(left_sensor, right_sensor)

navigator = Navigator(motors, line_sensor)

# Grabber setup
tilt_servo = Servo(config.TILT_SERVO_PIN, config.SERVO_FREQ)
jaw_servo = Servo(config.JAW_SERVO_PIN, config.SERVO_FREQ)
grabber = Grabber(tilt_servo, jaw_servo)

button = Button(config.START_BUTTON_PIN)
led_1 = LED(config.LED_1_PIN)
led_2 = LED(config.LED_2_PIN)
led_3 = LED(config.LED_3_PIN)
led_4 = LED(config.LED_4_PIN)

led_panel = LEDPanel([led_1, led_2, led_3, led_4])

resistance_measurer = ResistanceMeasurer(config.ADC_PIN_NUMBER)

# Home the grabber before starting
grabber.home()

# simple loop to test the resistance measurement before starting the main routine (waiting for the button to be pressed)
while not button.pressed():
    sleep_ms(100)

# Leave start box
navigator.leave_start_box()

# navigator.go_to_pickup_bay(1)

# navigator.go_to_rack(1)

# navigator.return_to_start_line()

for bay_number in range(1, 2):
    led_panel.all_off()

    # Go to pickup bay
    navigator.go_to_pickup_bay(bay_number)

    # Pick up box
    grabber.pick()

    sleep_ms(500)
    
    resistance_number = resistance_measurer.measure_resistance()

    led_panel.on(resistance_number)

    rack_number = [2, 1, 3, 4][resistance_number - 1]

    # Go to rack
    navigator.go_to_rack(rack_number)

    # find an empty rack slot & place the box down
    for i in range(6):
        if rack_number == 1 or rack_number == 3:
            navigator.line_follow_until(0, 1, config.BOX_DETECTING_SPEED)
        else:
            navigator.line_follow_until(1, 0, config.BOX_DETECTING_SPEED)
        
        if box_detector.rack_occupied(rack_number):
            if rack_number == 1 or rack_number == 3:
                navigator.skip_junction(0, 1)
            else:
                navigator.skip_junction(1, 0)
        else:
            navigator.approach_rack()
            grabber.open_part()
            navigator.exit_rack()
            grabber.home()
            break

    navigator.return_to_start_line()

# Return to start box
navigator.go_to_pickup_bay(0)
navigator.enter_start_box()
