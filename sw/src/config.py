# config.py  (Pico filesystem root)

# --- Line sensors (4 sensors, left -> right) ---
# Update these to the GPIO pins your 4 line sensors are wired to (left->right order)
LINE_PINS = [18, 19, 20, 21]
LINE_WHITE_IS_1 = True  # set False if your sensors output 0 on white and 1 on black

# --- Motors ---
# Update these to match your motor driver wiring (DIR pin + PWM pin for each motor)
LEFT_DIR_PIN = 4
LEFT_PWM_PIN = 5
RIGHT_DIR_PIN = 7
RIGHT_PWM_PIN = 6

# If your motors spin the wrong way, flip one (or both) of these
LEFT_INVERT_DIR = False
RIGHT_INVERT_DIR = False

# --- Control tuning ---
BASE_SPEED = 0.55   # 0..1
KP = 0.30
KD = 0.05
TURN_LIMIT = 1.0    # max magnitude of turn command

# Speed clamp (start with no reverse while tuning)
MIN_SPEED = 0.0     # 0..1 (set <0 only if you want reverse allowed)
MAX_SPEED = 1.0

# Loop timing
LOOP_DELAY_MS = 10  # 10ms = 100 Hz loop

# Box detection
BAY_OCCUPIED_THRESHOLD_MM = 180
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
