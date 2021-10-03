import analogio   # AnalogIn
import digitalio  # onboard led
import board
import time
import adafruit_dht

# setup onboard Led
led = digitalio.DigitalInOut(board.RED_LED)  # general-purpose RED LED on Pin D3
led.direction = digitalio.Direction.OUTPUT

# setup button, digitla in
btn = digitalio.DigitalInOut(board.D5)  # nRF52840, Grove D2
btn.direction = digitalio.Direction.INPUT
btn.pull = digitalio.Pull.DOWN

# setup poti, analog in
poti = analogio.AnalogIn(board.A0)  # nRF52840 A0, Grove A0

# setup dht, analog in
dht = adafruit_dht.DHT11(board.D9)  # nRF52840, Grove D4

# Constants
INTERVAL = 5  # time for measuring interval
WEIGHT = 5000  # 5kg -> 5000g, Poti Anzeige von 0-5000g

# Variable
treshhold_weight = 2500  # set at startup in mid of poti
measure_on_startup = True
run_once = True

# Main Loop
while True:
    # Measuring every INTERVAL Second
    #################################################################
    # run_once flag to make sure it doesnt run more often
    # start % 5 = True when start = xxxx5
    start = round(time.time())
    t = time.localtime(start)

    if start % INTERVAL == 0 and run_once or measure_on_startup:

        try:
            # Read the temperature and convert it to integer
            temperature = int(round(dht.temperature))
            # Read the humidity and convert it to integer
            humidity = int(round(dht.humidity))

            # Read Potentiometer value
            value = poti.value
            # Turn read values on Poti, left=0 : right=5000
            weight = int(round(WEIGHT-((value * WEIGHT) / 65536)))

            # Print timestamp, temperatur, humidity
            print("{:d}:{:02d}:{:02d}- Temp:{:g}, Hum:{:g}, Weight:{:d}, threshold:{:d}".format(
                t.tm_hour, t.tm_min, t.tm_sec, temperature, humidity, weight, treshhold_weight))

        except RuntimeError as e:
            # Reading doesn't always work! Just print error and we'll try again
            print("{:d}:{:02d}:{:02d}- Temp:{:g}, Hum:{:g}, Weight:{:d}, threshold:{:d}".format(
                t.tm_hour, t.tm_min, t.tm_sec, -1, -1, -1, -1))

        # set run_once flag false
        run_once = False

    # reset run_once flag
    if start % INTERVAL != 0:
        run_once = True

    # Run not time sensitiv code here (Input listener)
    ############################################################
    # Set check_weight: weight of dryed plant by pressing button
    if btn.value:
        treshhold_weight = weight
        print(f'button pressed new threshold = {treshhold_weight}')

    # Check if plant needs water: Turn on onboard led
    if weight <= treshhold_weight:
        led.value = True
    else:
        led.value = False

    # Read Potentiometer value -> plant weight
    value = poti.value
    # Turn read values on Poti, left=0 : right=5000
    weight = int(round(WEIGHT-((value * WEIGHT) / 65536)))
    print(f'weight: {weight}, threshhold: {treshhold_weight}')

    # Set measure_on_startup false
    measure_on_startup = False

    # Wait
    time.sleep(0.2)




###########
# infos
###########
# Grove Board Layout - https://github.com/tamberg/fhnw-idb/wiki/Grove-Adapters
