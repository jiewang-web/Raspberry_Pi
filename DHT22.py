import sys
import Adafruit_DHT
import time

while True:
    sensor = Adafruit_DHT.DHT22
    pin = 9
    time.sleep(2.5)
    # Try to grab a sensor reading.
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

    if humidity is not None and temperature is not None:
        print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))

