from utime import sleep
import config
from drivers.line_sensor import LineSensorArray

lsa = LineSensorArray(config.LINE_PINS, white_is_1=config.LINE_WHITE_IS_1)

while True:
    raw = lsa.read_raw()
    err = lsa.line_error()
    print("raw:", raw, "err:", err)
    sleep(0.1)