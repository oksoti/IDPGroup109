from .. import config
from utime import sleep_ms

class Navigator:
    def __init__(self, motors, line_sensor):
        self.motors = motors
        self.line_sensor = line_sensor
        self.rack_number = 0 # which rack the robot is at (0 = start box, a lower, a upper, b lower, b upper)
        self.bay_number = 0  # which bay the robot is at (0 = start box, 1-4)

    def turn_left(self):
        self.motors.drive(config.INSIDE_TURN_SPEED, config.OUTSIDE_TURN_SPEED)
        sleep_ms(config.LEFT_TURN_DURATION)
        self.motors.stop()

    def turn_right(self):
        self.motors.drive(config.OUTSIDE_TURN_SPEED, config.INSIDE_TURN_SPEED)
        sleep_ms(config.RIGHT_TURN_DURATION)
        self.motors.stop()

    def turn_around(self, clockwise=True):
        direction = 1 if clockwise else -1
        self.motors.drive(config.TURN_AROUND_SPEED * direction, -config.TURN_AROUND_SPEED * direction)
        sleep_ms(config.TURN_AROUND_DURATION)
        self.motors.stop()

    def line_follow_until(self, ol_target, or_target, speed=config.BASE_SPEED, reverse=False):
        direction = -1 if reverse else 1
        while True:
            ol, ml, mr, or_ = self.line_sensor.read_named()

            if ol == ol_target and or_ == or_target:
                self.motors.stop()
                break

            if ml == 1 and mr == 1:
                self.motors.drive(speed * direction, speed * direction)
            elif ml == 1 and mr == 0:
                self.motors.drive(speed * config.REALIGN_MULTIPLIER * direction, speed * direction)
            elif ml == 0 and mr == 1:
                self.motors.drive(speed * direction, speed * config.REALIGN_MULTIPLIER * direction)
            else:
                self.motors.stop()

            sleep_ms(10)
        self.motors.stop()

    def line_follow_for_duration(self, duration, speed=config.BASE_SPEED, reverse=False):
        direction = -1 if reverse else 1
        for _ in range(duration // 10):
            ol, ml, mr, or_ = self.line_sensor.read_named()

            if ml == 1 and mr == 1:
                self.motors.drive(speed * direction, speed * direction)
            elif ml == 1 and mr == 0:
                self.motors.drive(speed * config.REALIGN_MULTIPLIER * direction, speed * direction)
            elif ml == 0 and mr == 1:
                self.motors.drive(speed * direction, speed *config.REALIGN_MULTIPLIER * direction)
            else:
                self.motors.stop()

            sleep_ms(10)
        self.motors.stop()

    def skip_junction(self, ol_target, or_target, quantity=1):
        for _ in range(quantity):
            self.line_follow_until(ol_target, or_target)
            self.line_follow_for_duration(int(200.0 / config.BASE_SPEED))

    def leave_start_box(self):
        self.motors.drive(config.BASE_SPEED, config.BASE_SPEED)
        while True:
            ol, ml, mr, or_ = self.line_sensor.read_named()
            if ol == 1 and or_ == 1:
                sleep_ms(int(200.0 / config.BASE_SPEED))
                break
            sleep_ms(10)
        self.motors.stop()

    def enter_start_box(self):
        self.motors.drive(config.BASE_SPEED, config.BASE_SPEED)
        sleep_ms(int(800.0 / config.BASE_SPEED))
        self.motors.stop()

    def go_to_pickup_bay(self, bay_number):
        if self.rack_number == 0:
            self.line_follow_until(1, 1)
            if bay_number < 3:
                self.turn_left()
                self.line_follow_until(1, 0)
                if bay_number == 1:
                    self.line_follow_until(1, 1)
                self.turn_left()
            else:
                self.turn_right()
                self.line_follow_until(0, 1)
                if bay_number == 4:
                    self.line_follow_until(1, 1)
                self.turn_right()
        elif self.rack_number == 4:
            self.line_follow_until(1, 0)
            if bay_number != 1:
                self.turn_left()
                if bay_number == 2:
                    self.line_follow_until(0, 1)
                elif bay_number == 3:
                    self.skip_junction(0, 1, 2)
                    self.line_follow_until(0, 1)
                elif bay_number == 4:
                    self.line_follow_until(1, 1)
                elif bay_number == 0:
                    self.skip_junction(0, 1)
                    self.line_follow_until(0, 1)
                self.turn_right()
        else:
            self.line_follow_until(0, 1)
            if bay_number != 4:
                self.turn_right()
                if bay_number == 3:
                    self.line_follow_until(1, 0)
                elif bay_number == 2:
                    self.skip_junction(1, 0, 2)
                    self.line_follow_until(1, 0)
                elif bay_number == 1:
                    self.line_follow_until(1, 1)
                elif bay_number == 0:
                    self.skip_junction(1, 0)
                    self.line_follow_until(1, 0)
                self.turn_left()
        if bay_number != 0:       
            self.line_follow_for_duration(config.BAY_ENTER_DURATION, config.BAY_ENTER_SPEED)
        self.bay_number = bay_number

    def drive_for_duration(self, duration, speed=config.BASE_SPEED, reverse=False):
        direction = -1 if reverse else 1
        self.motors.drive(speed * direction, speed * direction)
        sleep_ms(duration)
        self.motors.stop()

    def approach_rack(self):
        if self.rack_number == 1 or self.rack_number == 3:
            self.turn_right()
        else:
            self.turn_left()
        self.line_follow_for_duration(config.RACK_APPROACH_DURATION, config.RACK_APPROACH_SPEED)

    def exit_rack(self):
        self.line_follow_until(1, 1, config.RACK_APPROACH_DURATION, True)
        if self.rack_number == 1 or self.rack_number == 3:
            self.turn_left()
        else:
            self.turn_right()

    def go_to_rack(self, rack_number):
        self.turn_around(self.bay_number > 2)
        if self.bay_number == 2 or self.bay_number == 3:
            self.line_follow_until(1, 1)
        elif self.bay_number == 1:
            self.line_follow_until(0, 1)
        else:
            self.line_follow_until(1, 0)
        
        if rack_number == 4:
            if self.bay_number < 4:
                self.turn_right()
                self.line_follow_until(1, 1)
                self.turn_left()
            else:
                self.skip_junction(1, 0)
        else:
            if self.bay_number > 1:
                self.turn_left()
                self.line_follow_until(1, 1)
                self.turn_right()
            else:
                self.skip_junction(0, 1)
            
            if rack_number > 1:
                self.line_follow_until(1, 1)
                self.line_follow_until(0, 1)
                self.turn_right()
                self.line_follow_until(0, 1)
                self.turn_right()
                self.line_follow_until(1, 1)
                if rack_number == 2:
                    self.turn_right()
                    self.line_follow_until(0, 1)
                    self.turn_right()
                else:
                    self.turn_left()
                    self.line_follow_until(1, 0)
                    self.turn_left()

        self.rack_number = rack_number

    def return_to_start_line(self):
        if self.rack_number == 2 or self.rack_number == 3:
            self.turn_around(self.rack_number == 3)
            if self.rack_number == 2:
                self.line_follow_until(1, 0)
                self.turn_left()
                self.line_follow_until(1, 0)
                self.turn_left()
            else:
                self.line_follow_until(0, 1)
                self.turn_right()
                self.line_follow_until(0, 1)
                self.turn_right()
            self.line_follow_until(1, 1)
            self.turn_right()
        else:
            self.line_follow_until(1, 1)

        if self.rack_number == 1:
            self.line_follow_until(0, 1)
            self.turn_right()
            self.skip_junction(0, 1)

        if self.rack_number == 4:
            self.line_follow_until(1, 0)
            self.turn_left()
            self.skip_junction(1, 0)
            self.line_follow_until(1, 0)
            self.turn_left()
            self.skip_junction(1, 1)
            self.skip_junction(1, 0, 6)
        else:
            self.line_follow_until(0, 1)
            self.turn_right()
            self.skip_junction(1, 1)
            self.skip_junction(0, 1, 6)
