from ..config import BASE_SPEED, REALIGN_SPEED
from utime import sleep_ms

class Navigator:
    def __init__(self, motors, line_sensor):
        self.motors = motors
        self.line_sensor = line_sensor
        self.rack_number = 0 # which rack the robot is at (0 = start box, a lower, a upper, b lower, b upper)
        self.bay_number = 0  # which bay the robot is at (0 = none, 1-4)

    def line_follow_until(self, ol_target, or_target, reverse=False):
        direction = -1 if reverse else 1
        while True:
            ol, ml, mr, or_ = self.line_sensor.read_named()

            if ol == ol_target and or_ == or_target:
                self.motors.stop()
                break

            if ml == 1 and mr == 1:
                self.motors.drive(BASE_SPEED * direction, BASE_SPEED * direction)
            elif ml == 1 and mr == 0:
                self.motors.drive(REALIGN_SPEED * direction, BASE_SPEED * direction)
            elif ml == 0 and mr == 1:
                self.motors.drive(BASE_SPEED * direction, REALIGN_SPEED * direction)
            else:
                self.motors.stop()

            sleep_ms(10)

    def skip_junction(self, ol_target, or_target, quantity=1):
        for _ in range(quantity):
            self.line_follow_until(ol_target, or_target)
            self.motors.drive(BASE_SPEED, BASE_SPEED)
            sleep_ms(200)  # drive forward past the junction
            self.motors.stop()

    def leave_start_box(self):
        self.motors.drive(BASE_SPEED, BASE_SPEED)
        while True:
            ol, ml, mr, or_ = self.line_sensor.read_named()
            if ol == 1 and or_ == 1:
                sleep_ms(200)
                break
            sleep_ms(10)

    def go_to_pickup_bay(self, bay_number):
        if self.rack_number == 0:
            self.line_follow_until(1, 1)
            if bay_number < 3:
                self.motors.turn_left(90)
                self.line_follow_until(1, 0)
                if bay_number == 1:
                    self.line_follow_until(1, 1)
                self.motors.turn_left(90)
            else:
                self.motors.turn_right(90)
                self.line_follow_until(0, 1)
                if bay_number == 4:
                    self.line_follow_until(1, 1)
                self.motors.turn_right(90)
        elif self.rack_number == 4:
            self.line_follow_until(1, 0)
            if bay_number > 1:
                self.motors.turn_left(90)
                if bay_number == 2:
                    self.line_follow_until(0, 1)
                elif bay_number == 3:
                    self.skip_junction(0, 1, 2)
                    self.line_follow_until(0, 1)
                elif bay_number == 4:
                    self.line_follow_until(1, 1)
                self.motors.turn_right(90)
        else:
            self.line_follow_until(0, 1)
            if bay_number < 4:
                self.motors.turn_right(90)
                if bay_number == 3:
                    self.line_follow_until(1, 0)
                elif bay_number == 2:
                    self.skip_junction(1, 0, 2)
                    self.line_follow_until(1, 0)
                elif bay_number == 1:
                    self.line_follow_until(1, 1)
                self.motors.turn_left(90)        
        self.line_follow_until(1, 1)
        self.bay_number = bay_number

    def go_to_rack(self, rack_number):
        self.motors.turn_around()
        if self.bay_number == 2 or self.bay_number == 3:
            self.line_follow_until(1, 1)
        elif self.bay_number == 1:
            self.line_follow_until(0, 1)
        else:
            self.line_follow_until(1, 0)
        
        if rack_number == 4:
            if self.bay_number < 4:
                self.motors.turn_right(90)
                self.line_follow_until(1, 1)
                self.motors.turn_left(90)
        else:
            if self.bay_number > 1:
                self.motors.turn_left(90)
                self.line_follow_until(1, 1)
                self.motors.turn_right(90)
            if rack_number > 1:
                self.line_follow_until(1, 1)
                self.line_follow_until(0, 1)
                self.motors.turn_right(90)
                self.line_follow_until(0, 1)
                self.motors.turn_right(90)
                self.line_follow_until(1, 1)
                if rack_number == 2:
                    self.motors.turn_right(90)
                    self.line_follow_until(0, 1)
                    self.motors.turn_right(90)
                else:
                    self.motors.turn_left(90)
                    self.line_follow_until(1, 0)
                    self.motors.turn_left(90)

        self.rack_number = rack_number

    def return_to_start_line(self):
        self.line_follow_until(1, 1)
        if self.rack_number == 2 or self.rack_number == 3:
            self.motors.turn_around()
            if self.rack_number == 2:
                self.line_follow_until(1, 0)
                self.motors.turn_left(90)
                self.line_follow_until(1, 0)
                self.motors.turn_left(90)
            else:
                self.line_follow_until(0, 1)
                self.motors.turn_right(90)
                self.line_follow_until(0, 1)
                self.motors.turn_right(90)
            self.line_follow_until(1, 1)
            self.motors.turn_right(90)

        if self.rack_number == 1:
            self.line_follow_until(0, 1)
            self.motors.turn_right(90)
            self.skip_junction(0, 1)

        if self.rack_number == 4:
            self.line_follow_until(1, 0)
            self.motors.turn_left(90)
            self.skip_junction(1, 0)
            self.line_follow_until(1, 0)
            self.motors.turn_left(90)
            self.skip_junction(1, 1)
            self.skip_junction(1, 0, 6)
        else:
            self.line_follow_until(0, 1)
            self.motors.turn_right(90)
            self.skip_junction(1, 1)
            self.skip_junction(0, 1, 6)

