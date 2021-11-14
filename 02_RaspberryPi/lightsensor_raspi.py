import time
from grove.grove_light_sensor_v1_2 import GroveLightSensor

pin = 4  # A4 Grove
lightsen = GroveLightSensor(pin)

LIGHT = 1000  # Dummy max Weight


while True:

    #light = int(round(lightsen.light * LIGHT / 999))
    print(lightsen.light)
    time.sleep(0.2)