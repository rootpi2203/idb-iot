import analogio
import board
import time


class Potentiometer():
    def __init__(self, data_pin):
        self.sensor = analogio.AnalogIn(data_pin)

    def read_value(self):
        value = self.sensor.value
        #voltage = (value * 3.3) / 65536
        #print((value, voltage)) # serial plotter format
        return value

    def read_value_0to1(self):
        reading = self.read_value()
        uniformed_reading = 1- float(reading) / 65535.0
        # reset to zero if almost reached, otherwise it may not be switching off 
        if(uniformed_reading < 0.05):
            uniformed_reading = 0
        #print(uniformed_reading)
        return uniformed_reading