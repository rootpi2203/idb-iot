import time
import board
import busio
import digitalio
from adafruit_esp32spi import adafruit_esp32spi
from adafruit_esp32spi import adafruit_esp32spi_socket
from adafruit_minimqtt import adafruit_minimqtt
from config import config

# TODO: Set your Wi-Fi ssid, password
wifi_ssid = config['ssid']
wifi_password = config['password']

# FeatherWing ESP32 AirLift, nRF52840
cs = digitalio.DigitalInOut(board.D13)
rdy = digitalio.DigitalInOut(board.D11)
rst = digitalio.DigitalInOut(board.D12)

spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
wifi = adafruit_esp32spi.ESP_SPIcontrol(spi, cs, rdy, rst)

while not wifi.is_connected:
    print("\nConnecting to Wi-Fi...")
    try:
        wifi.connect_AP(wifi_ssid, wifi_password)
    except RuntimeError as e:
        print("Cannot connect to Wi-Fi", e)
        continue

print("Wi-Fi connected to", str(wifi.ssid, "utf-8"))
print("IP address", wifi.pretty_ip(wifi.ip_address))

# MQTT setup
#mqtt_broker = "test.mosquitto.org"
#mqtt_topic = "hello"
mqtt_broker = config['ipraspi']
mqtt_topic = "/test/topic"

#my_message = None

def handle_connect(client, userdata, flags, rc):
    print("MQTT Connected to {0}".format(client.broker))
    mqtt_client.subscribe(mqtt_topic)

def handle_subscribe(client, userdata, topic, granted_qos):
    print("MQTT Subscribed to {0} with QOS {1}".format(topic, granted_qos))

def handle_message(client, topic, message):
    print("MQTT Received on {0}: {1}".format(topic, message))
    #print(dtypes(message)
    global my_message
    my_message = message

adafruit_minimqtt.set_socket(adafruit_esp32spi_socket, wifi)

mqtt_client = adafruit_minimqtt.MQTT(broker=mqtt_broker, port=1883,  is_ssl=False)

# Set callback handlers
mqtt_client.on_connect = handle_connect
mqtt_client.on_subscribe = handle_subscribe
mqtt_client.on_message = handle_message

print("\nMQTT Connecting to {0}".format(mqtt_broker))
mqtt_client.connect()

while True:
    mqtt_client.loop()
    time.sleep(3)
    #print(mqtt_client.on_message)
    print(my_message)
    #your code here :-)
