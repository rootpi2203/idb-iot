import time
import grovepi

button = 5

grovepi.pinMode(button, 'INPUT')

while True:
    print(grovepi.digitalRead(button))