# coding:utf-8
import RPi.GPIO as GPIO
import Adafruit_DHT as dht
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from time import sleep
from datetime import date, datetime
 
# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO_PIR = 23
GPIO.setup(GPIO_PIR,GPIO.IN)
#GPIO.cleanup()
 
# AWS IoT certificate based connection
myMQTTClient = AWSIoTMQTTClient("123afhlss411")
myMQTTClient.configureEndpoint("a130ba174k0fld-ats.iot.us-west-2.amazonaws.com", 8883)
myMQTTClient.configureCredentials("/home/pi/my_rpi/VeriSign-Class3-Public-Primary-Certification-Authority-G5.pem", "/home/pi/my_rpi/78755df119-private.pem.key", "/home/pi/my_rpi/78755df119-certificate.pem.crt")
myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
 
#connect and publish
myMQTTClient.connect()
myMQTTClient.publish("homepi/sensors", "connected", 0)
 
#loop and publish sensor reading
while True:
    now = datetime.utcnow()
    now_str = now.strftime('%Y-%m-%dT%H:%M:%SZ') #e.g. 2016-04-18T06:12:25.877Z
    h,t = dht.read_retry(dht.DHT22, 9) #09 pin is GPIO09
    if humidity is not None and temperature is not None:
        print ('Temp = %.1f"C, Humidity = %.1f%%RH' % (t, h))
    else:
        print('Failed to get reading. Try again!')
        sys.exit(1)
    Current_State = GPIO.input(GPIO_PIR)
    if Current_State == 1:
        rt = "A remider: the window is not closed"
        print ("A remider: the window is not closed")
    else:
        rt = "Good job! The window is closed"
        print ("Good job! The window is closed")
    payload = '{ "timestamp": "' + now_str + '"\n"temperature": ' + "{:.2f}".format(t)+ ',"humidity": '+ "{:.2f}".format(h) + '\n' + rt +' }'
    print ("payload")
    myMQTTClient.publish("homepi/sensors", payload, 0)
    sleep(10)