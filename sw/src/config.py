# config.py  (Pico filesystem root)

# --- Line sensors (4 sensors, left -> right) ---
# Update these to the GPIO pins your 4 line sensors are wired to (left->right order)
LINE_PINS = [18, 19, 20, 21]

# --- Motors ---
# Update these to match your motor driver wiring (DIR pin + PWM pin for each motor)
LEFT_DIR_PIN = 4
LEFT_PWM_PIN = 5
RIGHT_DIR_PIN = 7
RIGHT_PWM_PIN = 6

# If your motors spin the wrong way, flip one (or both) of these
LEFT_INVERT_DIR = False
RIGHT_INVERT_DIR = False

START_BUTTON_PIN = 22
LED_1_PIN = 12
LED_2_PIN = 14
LED_3_PIN = 16
LED_4_PIN = 17

BASE_SPEED = 1.0
REALIGN_SPEED = 0.3
OUTSIDE_TURN_SPEED = 1.0
INSIDE_TURN_SPEED = -0.2 * OUTSIDE_TURN_SPEED
TURN_AROUND_SPEED = 1.0

LEFT_TURN_DURATION = int(1100.0 / OUTSIDE_TURN_SPEED)
RIGHT_TURN_DURATION = int(1000.0 / OUTSIDE_TURN_SPEED)
TURN_AROUND_DURATION = int(1300.0 / TURN_AROUND_SPEED)

# Loop timing
LOOP_DELAY_MS = 10  # 10ms = 100 Hz loop

# Box detection
BAY_OCCUPIED_THRESHOLD_MM_LEFT = 275
BAY_OCCUPIED_THRESHOLD_MM_RIGHT = 250
BOX_SAMPLES = 7
BOX_SAMPLE_DELAY_MS = 10

BAY_TURN_DEG = 90          # or whatever you need to enter a bay
BAY_TURN_SPEED = 0.5
BAY_MS_PER_DEG = 12
BAY_APPROACH_SPEED = 25
BAY_APPROACH_MS = 80
BAY_SKIP_SPEED = 30
BAY_SKIP_MS = 200
BAY_TURN_SPEED = 35
BAY_SETTLE_MS = 30

I2C_ID_left = 0
I2C_SDA_PIN_left = 8
I2C_SCL_PIN_left = 9
I2C_FREQ_left = 400000

I2C_ID_right = 1
I2C_SDA_PIN_right = 10
I2C_SCL_PIN_right = 11
I2C_FREQ_right = 100000

SERVO_1_PIN = 13
SERVO_2_PIN = 15
SERVO_FREQ = 50
