from sw.tests.test_led import test_led
from test_led_pwm import test_led_pwm
from sw.tests.test_input import test_input_poll
from sw.tests.test_motor import test_motor3
from sw.tests.test_linear_actuator import test_actuator1
from sw.tests.test_tcs3472 import test_tcs3472
from sw.tests.test_vl53l0x import test_vl53l0x
from sw.tests.test_mfrc522 import test_mfrc522
from sw.tests.test_TMF8x01_get_distance import test_TMF8x01_get_distance
from sw.tests.test_STU_22L_IO_Mode import test_STU_22L_IO_Mode
from sw.tests.test_STU_22L_UART import test_STU_22L_UART
from sw.tests.test_tiny_code_reader import test_tiny_code_reader

print("Welcome to main.py!")

# Uncomment the test to run
# test_led()
# test_led_pwm()
# test_input_poll()
# test_motor3()
# test_tcs3472()
# test_actuator1()
# test_vl53l0x()
# test_mfrc522()
# test_TMF8x01_get_distance()
# test_STU_22L_IO_Mode()
# test_STU_22L_UART()
# test_tiny_code_reader()

from drivers.motor import error_to_motor_speeds

turn = controller.update(error)
left, right = error_to_motor_speeds(turn, base=0.55)
motors.drive(left, right)

print("main.py Done!")
