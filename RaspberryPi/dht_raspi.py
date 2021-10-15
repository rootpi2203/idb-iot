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
import grove.grove_temperature_humidity_sensor as dht

# setup dht, analog in
dht11 = dht.DHT('11', 5)  # Pi, Grove D5


# Main Loop
while True:

    humi, temp = dht11.read()
    print(humi, temp)


    time.sleep(1)