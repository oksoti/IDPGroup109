# sw/src/controllers/bay_controller.py
from utime import sleep_ms

class BayController:
    def __init__(self, drivetrain, box_detector, cfg):
        self.drive = drivetrain
        self.detector = box_detector
        self.cfg = cfg

    def attempt_turn_into_bay(self, direction):
        c = self.cfg

        # Stabilise for ranging
        self.drive.set_speeds(c.BAY_APPROACH_SPEED, c.BAY_APPROACH_SPEED)
        sleep_ms(c.BAY_APPROACH_MS)
        self.drive.stop()
        sleep_ms(c.BAY_SETTLE_MS)

        # Occupancy check
        if self.detector.object_confirmed():
            self.drive.set_speeds(c.BAY_SKIP_SPEED, c.BAY_SKIP_SPEED)
            sleep_ms(c.BAY_SKIP_MS)
            return False

        # Turn in
        if direction == "left":
            self.drive.turn_left(c.BAY_TURN_SPEED)
        else:
            self.drive.turn_right(c.BAY_TURN_SPEED)

        sleep_ms(c.BAY_TURN_MS)
        self.drive.stop()
        sleep_ms(c.BAY_SETTLE_MS)

        return True