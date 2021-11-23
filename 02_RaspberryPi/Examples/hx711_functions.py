import RPi.GPIO as GPIO
from hx711 import HX711
# credits to https://github.com/gandalf15/HX711/blob/master/python_examples/all_methods_example.py

def check_setup(hx):
    current_gain_A = hx.get_current_gain_A()
    current_channel = hx.get_current_channel()
    current_offset = hx.get_current_offset()
    current_scale_ratio = hx.get_current_scale_ratio()
    setup_dict = {'current_gain_A' : current_gain_A,
                  'current_channel' : current_channel,
                  'current_offset' : current_offset,
                  'current_scale_ratio' : current_scale_ratio}
    return setup_dict

def read_data(hx, reads=30):
    # Read data several, or only one, time and return mean value.
    # It subtracts offset value for particular channel from the mean value.
    # This value is still just a number from HX711 without any conversion
    # to units such as grams or kg.
    data = hx.get_data_mean(readings=reads)
    return data

def read_weight(hx, reads=30):
    return int(hx.get_weight_mean(30))

def set_scale(hx, weight=50, reads=30):
    if weight > 0:
        data = hx.get_data_mean(readings=reads)
        if data:
            ratio = data / weight  # calculate the ratio for channel A and gain 64
            hx.set_scale_ratio(ratio)  # set ratio for current channel
            print('Ratio is set.')
        else:
            raise ValueError('Cannot calculate mean value.')
        print(f'Current weight on the scale in grams is: {round(hx.get_weight_mean(30), 0)}g')

