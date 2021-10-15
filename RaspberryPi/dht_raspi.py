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
################################################################################

import time
from grove.grove_led import GroveLed
import grove.grove_temperature_humidity_sensor as dht
#from grove.factory import Factory

# setup button, digitla in
#btn = Factory.getButton('GPIO_HIGH', 16)  # Pi, Grove D16

# setup dht, analog in
dht11 = dht.DHT('11', 5)  # Pi, Grove D5


# Constants
INTERVAL = 5   # time interval. Measurement every Interval second
start_t1 = 0   # temp storage time
WEIGHT = 5000  # 5kg -> 5000g, Poti Anzeige von 0-5000g
LIGHT = 1000   # Lumen dummy calculation


# Main Loop
while True:
    # Measuring every INTERVAL Second
    #################################################################
    start = round(time.time())
    t = time.localtime(start)

    humi, temp = dht11.read()
    print(humi, temp)

    #if btn.is_pressed():
    #print('Button is pressed')


    time.sleep(1)