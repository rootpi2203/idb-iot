import time
from grove.factory import Factory

pin = 12
button = Factory.getButton("GPIO-HIGH", pin)

while True:
    if button.is_pressed():
        print('Button is pressed')
    else:
        print('Button is released')
    time.sleep(1)