from utime import sleep_ms

class BayController:
    def __init__(self, drivetrain, box_detector, cfg):
        self.drive = drivetrain
        self.detector = box_detector
        self.cfg = cfg

    def attempt_turn_into_bay(self, direction):
        c = self.cfg

        # Stabilise for ranging
        self.drive.drive(c.BAY_APPROACH_SPEED, c.BAY_APPROACH_SPEED)
        sleep_ms(c.BAY_APPROACH_MS)
        self.drive.stop()
        sleep_ms(c.BAY_SETTLE_MS)

        # Occupancy check
        if self.detector.object_confirmed():
            self.drive.drive(c.BAY_SKIP_SPEED, c.BAY_SKIP_SPEED)
            sleep_ms(c.BAY_SKIP_MS)
            self.drive.stop()
            sleep_ms(c.BAY_SETTLE_MS)
            return False

        # Turn in (MotorPair.turn_left/right already sleeps + stops)
        if direction == "left":
            self.drive.turn_left(
                c.BAY_TURN_DEG,
                turn_speed=c.BAY_TURN_SPEED,
                ms_per_deg=c.BAY_MS_PER_DEG
            )
        elif direction == "right":
            self.drive.turn_right(
                c.BAY_TURN_DEG,
                turn_speed=c.BAY_TURN_SPEED,
                ms_per_deg=c.BAY_MS_PER_DEG
            )
        else:
            raise ValueError("direction must be 'left' or 'right'")

        sleep_ms(c.BAY_SETTLE_MS)
        return True