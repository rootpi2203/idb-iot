###########
# Mini Challenge idb HS21 - Manuel Schwarz
# Messungen: Gewicht, Temperatur, Luftfeuchtigkeit und Lichtstärke messen
# mit button die Gewichtsgrenze festlegen. Fällt das Gewicht darunter wird
# die led eingeschaltet -> Pflanze benötigt Wasser.
###########
# Grove Board Layout pi - https://github.com/tamberg/fhnw-idb/wiki/Grove-Adapters#mapping
# button        -> Grove D5
# potentiometer -> Grove A0
# dht           -> Grove D16
# light_sen     -> Grove A4
# led           -> Grove A2
# hx711 load    -> Grove PWM (dout_pin=13, clk=12
################################################################################

import time
from grove.grove_led import GroveLed
from grove.factory import Factory
from grove.grove_slide_potentiometer import GroveSlidePotentiometer
import seeed_dht
from grove.grove_light_sensor_v1_2 import GroveLightSensor
import RPi.GPIO as GPIO
from hx711 import HX711
# credits to https://github.com/gandalf15/HX711/blob/master/python_examples/all_methods_example.py

######## Hardware - Pin Belegung (Grove Board) ##
button_pin = 5
poti_pin = 0
dht11_pin = 16
light_pin = 4
#led_pin = 12
hx711_dout_pin = 13
hx711_sck_pin = 12

######## Setup #######################
#led = GroveLed(12)  # Pi, Grove, setup Led, digital out
btn = Factory.getButton("GPIO-HIGH", button_pin)  # Pi, Grove D5, setup button, digitla in
poti = GroveSlidePotentiometer(poti_pin)  # Pi, Grove A0, setup Potentiometer
dht11 = seeed_dht.DHT('11', dht11_pin)  # Pi, Grove D16, setup dht, analog in
light_sen = GroveLightSensor(light_pin)  # setup light sensor
hx = HX711(hx711_dout_pin, hx711_sck_pin)  # Weight scale

# Constants
INTERVAL_SENSOR_READING = 5   # time interval. Measurement every Interval second
INTERVAL_MAIN_LOOP = 0.5
NR_LOOPS = INTERVAL_SENSOR_READING / INTERVAL_MAIN_LOOP
_counter = NR_LOOPS
start_t1 = 0   # temp storage time
WEIGHT = 5000  # 5kg -> 5000g, Poti Anzeige von 0-5000g
weight = 2400  # dummy
#LIGHT = 1000   # Lumen dummy calculation
treshhold_weight = 150  # set at startup (mid of poti)
TIME_SLEEP = 1
start_up = True

####### Functions ##################
def read_dht():
    temp, hum = dht11.read()
    return temp, hum

def read_light():
    return light_sen.light

def check_setup():
    current_gain_A = hx.get_current_gain_A()
    current_channel = hx.get_current_channel()
    current_offset = hx.get_current_offset()
    current_scale_ratio = hx.get_current_scale_ratio()
    setup_dict = {'current_gain_A' : current_gain_A,
                  'current_channel' : current_channel,
                  'current_offset' : current_offset,
                  'current_scale_ratio' : current_scale_ratio}
    return setup_dict

def set_scale(weight=50, reads=30):
    if weight > 0:
        data = hx.get_data_mean(readings=reads)
        if data:
            ratio = data / weight  # calculate the ratio for channel A and gain 64
            hx.set_scale_ratio(ratio)  # set ratio for current channel
            print('Ratio is set.')
        else:
            raise ValueError('Cannot calculate mean value.')
        print(f'Current weight on the scale in grams is: {round(hx.get_weight_mean(30), 0)}g')

def read_weight(reads=30):
    return int(hx.get_weight_mean(reads))

def print_val(Temp, Hum, light, Weight, threshhold_weight):
    t = time.localtime(time.time())
    print("{:d}:{:02d}:{:02d}- Temp:{:g}, Hum:{:g}, Light:{:d}, Weight:{:d}, threshhold: {:d}".format(
        t.tm_hour, t.tm_min, t.tm_sec, Temp, Hum, light, Weight, threshhold_weight))

def button_pressed():
    pass

def toggle_led():
    pass

def post_http():
    pass

def isTimerExpired():
    global _counter
    if _counter <= 1:
        _counter = NR_LOOPS
        return True
    else:
        _counter = _counter - 1
        return False


##### startup ####
print(check_setup())  # check setup
set_scale(weight=100)  # set known load to scale

while True:
    # Measuring every INTERVAL Second
    #################################################################
    t = time.localtime(time.time())
    start_meas = time.monotonic()  # timing measurement start
    if isTimerExpired() or start_up:
        try:
            temp, hum = read_dht()   # Read the temperature + humidity
            light = read_light()  # Read Light sensor
            weight = read_weight(reads=30)  # reads the mean from 30 values from hx711 (30-> 3sec)
            print_val(temp, hum, light, weight, treshhold_weight)

        except RuntimeError as e:
            print_val(-1, -1, -1, -1, -1)

    end_meas = time.monotonic()  # timing measurement end
    start_up = False
    measure_time = end_meas - start_meas
    if INTERVAL_MAIN_LOOP >= measure_time:
        time.sleep(INTERVAL_MAIN_LOOP - measure_time)

    # Run not time sensitiv code here (Input listener)
    ############################################################
    # Set check_weight: weight of dryed plant by pressing button
    if btn.is_pressed():
        treshhold_weight = weight
        print(f'button pressed new threshold = {treshhold_weight}')

    # Check if plant needs water: Turn on onboard led
    if weight <= treshhold_weight:
        print('Gewicht zu tief -> Pflanze benötigt Wasser')
        #led.on()
    #else:
        #led.off()

    # Change and read values on Poti, left=0 : right=5000
    weight = read_weight(reads=10)
    print(f'weight: {weight}, threshhold: {treshhold_weight}')