import time
from grove.grove_led import GroveLed

# setup
pin_led = 12  #Grove PWM D12
led = GroveLed(pin_led)

while True:
    led.on()
    print("on")
    time.sleep(0.5)
    led.off()
    time.sleep(0.2)
    print("off")