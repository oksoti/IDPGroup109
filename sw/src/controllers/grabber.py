from src.drivers.servo import Servo
import src.config as config
from utime import sleep_ms

class Grabber:

    def __init__(
        self,
        tilt_servo,
        jaw_servo,
        tilt_down=80,
        tilt_up=130,
        tilt_home=150,
        jaw_open_full=70,
        jaw_open_part=20,
        jaw_closed=10,
        jaw_home=10
    ):
        self.tilt_servo = tilt_servo
        self.jaw_servo = jaw_servo

        # preset angles
        self.tilt_down = tilt_down
        self.tilt_up = tilt_up
        self.tilt_home = tilt_home
        self.jaw_open_full = jaw_open_full
        self.jaw_open_part = jaw_open_part
        self.jaw_closed = jaw_closed
        self.jaw_home = jaw_home

        # track the current angle of each servo so we can move them incrementally between positions
        self._tilt_angle = tilt_home
        self._jaw_angle = jaw_home

    def set_tilt(self, desired_angle): # set the angle of the tilt servo
        self.tilt_servo.set_angle(self._tilt_angle, desired_angle)
        self._tilt_angle = desired_angle

    def set_jaw(self, desired_angle): # set the angle of the jaw servo
        self.jaw_servo.set_angle(self._jaw_angle, desired_angle)
        self._jaw_angle = desired_angle

    # Several functions to move either servo to certain pre-programmed angles #
    def tilt_upwards(self):
        self.set_tilt(self.tilt_up)

    def tilt_downwards(self):
        self.set_tilt(self.tilt_down)

    def open_part(self): # dropping a reel
        self.set_jaw(self.jaw_open_part)

    def open_full(self): # for picking up a reel
        self.set_jaw(self.jaw_open_full)

    def close(self):
        self.set_jaw(self.jaw_closed)

    def home(self):
        self.set_tilt(self.tilt_home)
        self.set_jaw(self.jaw_home)
