import time
import adafruit_dht
import board
import digitalio

# Constants
INTERVAL_SENSOR_READING=5   # sec
INTERVAL_MAIN_LOOP = 0.5      # sec
NR_LOOPS = INTERVAL_SENSOR_READING / INTERVAL_MAIN_LOOP

# Setup
dht = adafruit_dht.DHT11(board.D9)  # nRF52840, Grove D4
led = digitalio.DigitalInOut(board.RED_LED)  # general-purpose RED LED on Pin D3
led.direction = digitalio.Direction.OUTPUT
led.value = True

_counter = NR_LOOPS

def readTemperature():
    # Read the temperature and convert it to integer
    return int(round(dht.temperature))

def readHumidity():
    # Read the humidity and convert it to integer
    return int(round(dht.humidity))

def printTempHum(temperature, humidity):
    t = time.localtime(time.time())
    print("{:d}:{:02d}:{:02d},{:g},{:g}".format(t.tm_hour, t.tm_min, t.tm_sec, temperature, humidity))

def toggleLed():
    led.value = not led.value

def isTimerExpired():
    global _counter
    if _counter <= 1:
        _counter = NR_LOOPS
        return True
    else:
        _counter = _counter - 1
        return False
    
# Main Loop (1sec)
while True:
    start = time.monotonic()

    # read sensors
    if isTimerExpired():
        try:
            temperature = readTemperature()
            humidity = readHumidity()
            printTempHum(temperature, humidity)
        except RuntimeError as e:
            pass

    # Wait for the remaining time
    end = time.monotonic()
    time.sleep(INTERVAL_MAIN_LOOP - (end - start))

    # write actors
    toggleLed()