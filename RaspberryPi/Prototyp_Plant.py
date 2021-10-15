###########
# readme
# Prototyp: Gewicht, Temperatur, Luftfeuchtigkeit und Lichtstärke messen
# mit button die Gewichtsgrenze festlegen. Fällt das Gewicht darunter wird
# die onboard led eingeschaltet.
###########
# Grove Board Layout pi - https://github.com/tamberg/fhnw-idb/wiki/Grove-Adapters#mapping
# button -> Grove D5
# potentiometer -> Grove A0
# dht -> Grove D16
# light_sen -> Grove A4
# led -> Grove PWM D12
################################################################################

import time
from grove.grove_led import GroveLed
from grove.factory import Factory
from grove.grove_slide_potentiometer import GroveSlidePotentiometer
import grove.grove_temperature_humidity_sensor as dht
from grove.grove_light_sensor_v1_2 import GroveLightSensor

######## Setup #######################

# setup Led, digital out
led = GroveLed(12)  # Pi, Grove PWM D12

# setup button, digitla in
btn = Factory.getButton('GPIO_HIGH', 5)  # Pi, Grove D5

# setup Potentiometer
poti = GroveSlidePotentiometer(0)  # Pi, Grove A0

# setup dht, analog in
dht11 = dht('11', 16)  # Pi, Grove D16

# setup light sensor
lightsen = GroveLightSensor(4)


# Constants
INTERVAL = 5   # time interval. Measurement every Interval second
start_t1 = 0   # temp storage time
WEIGHT = 5000  # 5kg -> 5000g, Poti Anzeige von 0-5000g
#LIGHT = 1000   # Lumen dummy calculation
treshhold_weight = 2500  # set at startup (mid of poti)


# Main Loop
while True:
    # Measuring every INTERVAL Second
    #################################################################
    start = round(time.time())
    t = time.localtime(start)

    if start - start_t1 > INTERVAL:
        try:
            # Read the temperature + humidity and convert it to integer
            temp, hum = int(round(dht.read()))

            # change read values on Poti, left=0 : right=5000 / default 0-999
            weight = int(round(WEIGHT-((poti.value * WEIGHT) / 999)))

            # Read Light sensor
            light = lightsen.light
            # calculate Lumen
            #light = int(round((light_value * LIGHT) / 65536))

            # Print timestamp, temperatur, humidity
            print("{:d}:{:02d}:{:02d}- Temp:{:g}, Hum:{:g}, Weight:{:d}, threshhold:{:d}, light: {:d}".format(
                t.tm_hour, t.tm_min, t.tm_sec, temp, hum, weight, treshhold_weight, light))

        except RuntimeError as e:
            # Reading doesn't always work! Just print error and we'll try again
            print("{:d}:{:02d}:{:02d}- Temp:{:g}, Hum:{:g}, Weight:{:d}, threshhold:{:d}, light: {:d}".format(
                t.tm_hour, t.tm_min, t.tm_sec, -1, -1, -1, -1, -1))

        # reset time
        start_t1 = start

    # Run not time sensitiv code here (Input listener)
    ############################################################
    # Set check_weight: weight of dryed plant by pressing button
    if btn.is_pressed():
        treshhold_weight = weight
        print(f'button pressed new threshold = {treshhold_weight}')

    # Check if plant needs water: Turn on onboard led
    if weight <= treshhold_weight:
        led.on()
    else:
        led.off()

    # Change and read values on Poti, left=0 : right=5000
    weight = int(round(WEIGHT-((poti.value * WEIGHT) / 999)))
    print(f'weight: {weight}, threshhold: {treshhold_weight}')

    # Wait
    time.sleep(0.2)