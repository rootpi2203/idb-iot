import board
import digitalio
import time
import os

# setup
led = digitalio.DigitalInOut(board.RED_LED)  # general-purpose RED LED on Pin D3
led.direction = digitalio.Direction.OUTPUT

while True:
    led.value = True
    print("on")
    time.sleep(2)
    led.value = False
    time.sleep(1)
    print("off")
