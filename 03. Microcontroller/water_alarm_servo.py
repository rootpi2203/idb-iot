'''
Connects to WIFI and MQTT Topic on RasperberryPi
Listen to every plant_measurement topic (plant1, *plant2, *plant3)
Checks Message and moves Serve (which has an attached arm)
'''
import time
import board
import busio
import digitalio
from adafruit_esp32spi import adafruit_esp32spi
from adafruit_esp32spi import adafruit_esp32spi_socket
from adafruit_minimqtt import adafruit_minimqtt
from config import config
# Servo
import pwmio
from adafruit_motor import servo

# TODO: Set your Wi-Fi ssid, password
wifi_ssid = config['ssid']
wifi_password = config['password']

# FeatherWing ESP32 AirLift, nRF52840
cs = digitalio.DigitalInOut(board.D13)
rdy = digitalio.DigitalInOut(board.D11)
rst = digitalio.DigitalInOut(board.D12)

spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
wifi = adafruit_esp32spi.ESP_SPIcontrol(spi, cs, rdy, rst)

# create a PWMOut object on Pin A2.
pwm = pwmio.PWMOut(board.A2, frequency=50)
my_servo = servo.ContinuousServo(pwm)
ARMMOVEMENT = 3

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
mqtt_topic = "/plant_measurement/#"

mqtt_message = {'topic':0, 'message':0}
alarm_message = 'help I need water'
alarm_status = 0

def handle_connect(client, userdata, flags, rc):
    print("MQTT Connected to {0}".format(client.broker))
    mqtt_client.subscribe(mqtt_topic)

def handle_subscribe(client, userdata, topic, granted_qos):
    print("MQTT Subscribed to {0} with QOS {1}".format(topic, granted_qos))

def handle_message(client, topic, message):
    print("MQTT Received on {0}: {1}".format(topic, message))
    global mqtt_message
    mqtt_message = {'topic':topic, 'message':message}

adafruit_minimqtt.set_socket(adafruit_esp32spi_socket, wifi)

mqtt_client = adafruit_minimqtt.MQTT(broker=mqtt_broker, port=1883,  is_ssl=False)

# Set callback handlers
mqtt_client.on_connect = handle_connect
mqtt_client.on_subscribe = handle_subscribe
mqtt_client.on_message = handle_message

print("\nMQTT Connecting to {0}".format(mqtt_broker))
mqtt_client.connect()

# Alarm Aktionen
def check_mqtt_message():
    global mqtt_message
    global alarm_status
    if mqtt_message['message'] == alarm_message:
        mqtt_message.update({'topic':0, 'message':0})
        alarm_status = 1
        print(f'alarm_status: {alarm_status}')

def check_alarm_status():
    global alarm_status
    if alarm_status == 0:
        return

    elif alarm_status == 1:
        servo_does_something()
        alarm_status = 0
        print(f'alarm_status: {alarm_status}')

    elif alarm_status == 2:
        pass

def servo_does_something():
    for i in range(ARMMOVEMENT):
        #print("forward")
        my_servo.throttle = 1
        time.sleep(1.0)
        my_servo.throttle = 0.0
        time.sleep(1.0)
        #print("reverse")
        my_servo.throttle = -1
        time.sleep(1.0)
        my_servo.throttle = 0.0


while True:
    mqtt_client.loop()  # Reads MQTT Topic
    check_mqtt_message()  # Check Message and write Alarm status
    check_alarm_status()  # Checks Alarm Status and react



