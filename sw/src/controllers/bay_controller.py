from utime import sleep_ms

class BayController:
    def __init__(self, drivetrain, left_detector, right_detector, cfg):
        self.drive = drivetrain
        self.left_detector = left_detector     # VL53L0X side
        self.right_detector = right_detector   # TMF8701 side
        self.cfg = cfg

    def bay_occupied(self, bay_number):
        # Bays 1-2: check RIGHT sensor (TMF8701)
        if bay_number in (1, 2):
            return self.right_detector.bay_occupied()
        # Bays 3-4: check LEFT sensor (VL53L0X)
        if bay_number in (3, 4):
            return self.left_detector.bay_occupied()
        raise ValueError("bay_number must be 1, 2, 3, or 4")

    def attempt_turn_into_bay(self, bay_number, direction):
        c = self.cfg

        # Stabilise for ranging
        self.drive.drive(c.BAY_APPROACH_SPEED, c.BAY_APPROACH_SPEED)
        sleep_ms(c.BAY_APPROACH_MS)
        self.drive.stop()
        sleep_ms(c.BAY_SETTLE_MS)

        # Occupancy check (correct side based on bay_number)
        if self.bay_occupied(bay_number):
            self.drive.drive(c.BAY_SKIP_SPEED, c.BAY_SKIP_SPEED)
            sleep_ms(c.BAY_SKIP_MS)
            self.drive.stop()
            sleep_ms(c.BAY_SETTLE_MS)
            return False

        # Turn in (MotorPair.turn_left/right already sleeps + stops)
        if direction == "left":
            self.drive.turn_left(c.BAY_TURN_DEG, turn_speed=c.BAY_TURN_SPEED, ms_per_deg=c.BAY_MS_PER_DEG)
        elif direction == "right":
            self.drive.turn_right(c.BAY_TURN_DEG, turn_speed=c.BAY_TURN_SPEED, ms_per_deg=c.BAY_MS_PER_DEG)
        else:
            raise ValueError("direction must be 'left' or 'right'")

        sleep_ms(c.BAY_SETTLE_MS)
        return True
