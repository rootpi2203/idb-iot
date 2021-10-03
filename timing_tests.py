# Write your code here :-)
import analogio   # AnalogIn
import digitalio  # onboard led
import board
import time
import adafruit_dht

# setup onboard Led
led = digitalio.DigitalInOut(board.RED_LED)  # general-purpose RED LED on Pin D3
led.direction = digitalio.Direction.OUTPUT

# setup button, digitla in
btn = digitalio.DigitalInOut(board.D5)  # nRF52840, Grove D2
btn.direction = digitalio.Direction.INPUT
btn.pull = digitalio.Pull.DOWN

# variable
run_loop_once = True

# Main Loop
while True:
    start = round(time.monotonic())
    print(f'loop time: {start}')

    # Measuring every x seconds
    if start % 5 == 0 and run_loop_once:
        print(f'measuring')
        print(run_loop_once)
        run_loop_once = False
    if start % 5 != 0:
        run_loop_once = True

    # check button function
    btn.value
    if btn.value:
        print(f'button pressed = {btn.value}')

    time.sleep(0.2)

###########
# infos
###########
# Grove Board Layout - https://github.com/tamberg/fhnw-idb/wiki/Grove-Adapters
