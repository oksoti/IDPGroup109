from src.drivers.servo import Servo
import src.config as config
from utime import sleep_ms

class Grabber:

    def __init__(
        self,
        tilt_servo,
        jaw_servo,
        tilt_down=80,
        tilt_up=115,
        tilt_home=150,
        jaw_open_full=70,
        jaw_open_part=33,
        jaw_closed=28,
        jaw_home=25
    ):
        self.tilt_servo = tilt_servo
        self.jaw_servo = jaw_servo

        # presets
        self.tilt_down = tilt_down
        self.tilt_up = tilt_up
        self.tilt_home = tilt_home
        self.jaw_open_full = jaw_open_full
        self.jaw_open_part = jaw_open_part
        self.jaw_closed = jaw_closed
        self.jaw_home = jaw_home

        # Grabber tracks current angles because Servo.set_angle needs them
        self._tilt_angle = tilt_home
        self._jaw_angle = jaw_home

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
        self.set_tilt(self.tilt_home)
        self.set_jaw(self.jaw_home)

    def pick(self):
        # Open -> lower -> close -> lift
        self.open_full()
        self.tilt_downwards()
        self.close()
        self.tilt_upwards()

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
    
