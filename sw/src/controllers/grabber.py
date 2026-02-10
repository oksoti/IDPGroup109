from src.drivers.servo import Servo
import src.config as config

class Grabber:

    def __init__(
        self,
        tilt_servo,
        jaw_servo,
        tilt_down=30,
        tilt_up=110,
        jaw_open=20,
        jaw_closed=85,
    ):
        self.tilt_servo = tilt_servo
        self.jaw_servo = jaw_servo

        # presets
        self.tilt_down = tilt_down
        self.tilt_up = tilt_up
        self.jaw_open = jaw_open
        self.jaw_closed = jaw_closed

        # Grabber tracks current angles because Servo.set_angle needs them
        self._tilt_angle = 0
        self._jaw_angle = 0

        # optional state
        self.jaw_is_open = None

    # ---------------- low-level setters (match Servo API) ----------------

    def set_tilt(self, desired_angle):
        """Move tilt servo to desired_angle, updating internal current angle."""
        self.tilt_servo.set_angle(self._tilt_angle, desired_angle)
        self._tilt_angle = desired_angle

    def set_jaw(self, desired_angle):
        """Move jaw servo to desired_angle, updating internal current angle."""
        self.jaw_servo.set_angle(self._jaw_angle, desired_angle)
        self._jaw_angle = desired_angle

    # ---------------- high-level actions ----------------

    def tilt_upwards(self):
        self.set_tilt(self.tilt_up)

    def tilt_downwards(self):
        self.set_tilt(self.tilt_down)

    def open(self):
        """Open jaws."""
        self.set_jaw(self.jaw_open)
        self.jaw_is_open = True

    def close(self):
        """Close jaws."""
        self.set_jaw(self.jaw_closed)
        self.jaw_is_open = False

    def toggle_jaw(self):
        """Toggle open <-> close."""
        if self.jaw_is_open is None:
            self.open()
        elif self.jaw_is_open:
            self.close()
        else:
            self.open()

    # ---------------- sequences ----------------

    def home(self):
        """Safe default pose."""
        self.tilt_upwards()
        self.open()

    def pick(self):
        """Open -> lower -> close -> lift."""
        self.open()
        self.tilt_downwards()
        self.close()
        self.tilt_upwards()

    def drop(self):
        """Lower -> open -> lift."""
        self.tilt_downwards()
        self.open()
        self.tilt_upwards()


    
