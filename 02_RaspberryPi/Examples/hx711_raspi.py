import time
import RPi.GPIO as GPIO
from hx711 import HX711
from hx711_functions import *
# credits to https://github.com/gandalf15/HX711/blob/master/python_examples/all_methods_example.py

GPIO.setmode(GPIO.BCM)
dout_pin = 6
pd_sck_pin = 5


hx = HX711(dout_pin, pd_sck_pin)

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


# check setup
print(check_setup())
# set known load to scale
set_scale(weight=100)

while True:
    start = time.time() # mean von 30 Messungen dauern ca. 3 sec!
    #check_setup()
    scale_weight = int(read_weight())

    end = time.time()
    print(scale_weight, end-start)
    #time.sleep(0.5)
