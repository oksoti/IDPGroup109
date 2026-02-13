from src.drivers.servo import Servo
import src.config as config
from utime import sleep_ms

class Grabber:

    def __init__(
        self,
        tilt_servo,
        jaw_servo,
        tilt_down=80,
        tilt_up=110,
        jaw_open_full=120,
        jaw_open_part=30,
        jaw_closed=20,
    ):
        self.tilt_servo = tilt_servo
        self.jaw_servo = jaw_servo

        # presets
        self.tilt_down = tilt_down
        self.tilt_up = tilt_up
        self.jaw_open_full = jaw_open_full
        self.jaw_open_part = jaw_open_part
        self.jaw_closed = jaw_closed

        # Grabber tracks current angles because Servo.set_angle needs them
        self._tilt_angle = tilt_up
        self._jaw_angle = jaw_open_full

    def set_tilt(self, desired_angle):
        """Move tilt servo to desired_angle, updating internal current angle."""
        self.tilt_servo.set_angle(self._tilt_angle, desired_angle)
        self._tilt_angle = desired_angle

    def set_jaw(self, desired_angle):
        """Move jaw servo to desired_angle, updating internal current angle."""
        self.jaw_servo.set_angle(self._jaw_angle, desired_angle)
        self._jaw_angle = desired_angle

    def tilt_upwards(self):
        self.set_tilt(self.tilt_up)

    def tilt_downwards(self):
        self.set_tilt(self.tilt_down)

    def open_part(self):
        # Open jaws partly for dropping into rack
        self.set_jaw(self.jaw_open_part)

    def open_full(self):
        # Open jaws fully for picking up boxes
        self.set_jaw(self.jaw_open_full)

    def close(self):
        """Close jaws."""
        self.set_jaw(self.jaw_closed)

    def home(self):
        # Safe default pose
        self.tilt_upwards()
        self.open_full()

    def pick(self):
        # Open -> lower -> close -> lift
        self.open_full()
        sleep_ms(100)
        self.tilt_downwards()
        sleep_ms(100)
        self.close()
        sleep_ms(100)
        self.tilt_upwards()
        sleep_ms(100)

    def drop(self):
        # Lower -> open -> lift
        self.tilt_downwards()
        sleep_ms(100)
        self.open_part()
        sleep_ms(100)
        self.tilt_upwards()

    def drop_box(self):
        self.drop()
        self.home()
    
