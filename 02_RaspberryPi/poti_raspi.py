import time
from grove.grove_slide_potentiometer import GroveSlidePotentiometer

pin = 0  # A0 Grove
poti = GroveSlidePotentiometer(pin)

WEIGHT = 5000  # Dummy max Weight


while True:

    weight = int(round(WEIGHT - ((poti.value * WEIGHT) / 999)))
    print(weight)
    time.sleep(0.2)