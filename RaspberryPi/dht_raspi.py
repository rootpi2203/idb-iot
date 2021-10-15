import time
import seeed_dht

# setup dht, analog in
#dht11 = dht.DHT('11', 16)  # Pi, Grove D16
dht11 = seeed_dht.DHT('11', 16)

# Main Loop
while True:

    humi, temp = dht11.read()
    print(humi, temp)


    time.sleep(1)