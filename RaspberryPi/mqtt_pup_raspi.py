import paho.mqtt.publish as publish
from config import config

MQTT_SERVER = 'localhost'  #config['ipraspi']
MQTT_PATH = "/test/topic"

publish.single(MQTT_PATH, "Hello save World!", hostname=MQTT_SERVER)

