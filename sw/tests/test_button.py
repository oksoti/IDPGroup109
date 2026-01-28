from machine import Pin
from utime import sleep

button = Pin(22, Pin.IN, Pin.PULL_DOWN)

toggle_state = False
last_button = 0

print("Program started")

while True:
    current = button.value()
    print("Button value:", current)

    # detect rising edge
    if current == 1 and last_button == 0:
        toggle_state = not toggle_state
        print("TOGGLED ->", toggle_state)

    last_button = current
    sleep(0.5)