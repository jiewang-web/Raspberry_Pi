import sys
import Adafruit_DHT
import time
import array

def DHT():
    try:
        while True:
            sensor = Adafruit_DHT.DHT22
            pin = 9
            time.sleep(1)
            humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
            humidity = round(humidity, 2)
            temperature = round(temperature, 2)
            if humidity is not None and temperature is not None:
                print('Humidity={1:0.1f}% Tempera={0:0.1f}* '.format(humidity, temperature))
            #ans.append(humidity)
            #ans.append(temperature)
            ans = [humidity, temperature]
            return ans #humidity, temperature
        
    except KeyboardInterrupt:
        print("\n DHT22 stopped by User")
        

