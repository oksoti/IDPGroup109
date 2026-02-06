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

    def attempt_turn_into_bay(self, bay_number):
        c = self.cfg

        # Stabilise for ranging
        self.drive.drive(c.BAY_APPROACH_SPEED, c.BAY_APPROACH_SPEED)
        sleep_ms(c.BAY_APPROACH_MS)
        self.drive.stop()
        sleep_ms(c.BAY_SETTLE_MS)

        # Occupancy check (correct side based on bay_number)
        if self.bay_occupied(bay_number):
            print(f"Bay {bay_number} is occupied, skipping turn")
            self.drive.drive(c.BAY_SKIP_SPEED, c.BAY_SKIP_SPEED)
            sleep_ms(c.BAY_SKIP_MS)
            self.drive.stop()
            sleep_ms(c.BAY_SETTLE_MS)
            return False

        # Turn in (MotorPair.turn_left/right already sleeps + stops)
        '''if direction == "left":'''
        '''if direction == "right":'''

        sleep_ms(c.BAY_SETTLE_MS)
        return True
