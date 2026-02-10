
class Grabber:
    def __init__(self, servo_1, servo_2):
        self.servo_1 = servo_1
        self.servo_2 = servo_2

    def open(self):
        self.servo_1.set_angle(0)  # Open position for servo 1
        self.servo_2.set_angle(0)  # Open position for servo 2

    def close(self):
        self.servo_1.set_angle(90)  # Closed position for servo 1
        self.servo_2.set_angle(90)  # Closed position for servo 2

    def toggle(self, is_open):
        if is_open:
            self.close()
        else:
            self.open()

    