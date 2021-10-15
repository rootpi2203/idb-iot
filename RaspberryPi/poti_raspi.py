import time
from grove.grove_slide_potentiometer as potentiometer

pin = 16
poti = potentiometer(pin)

WEIGHT = 5000

while True:
    poti.read()
    time.sleep(1)