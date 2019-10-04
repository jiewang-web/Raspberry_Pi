#!/usr/bin/python
# Filename: sensor.py
import RPi.GPIO as GPIO
import time
import sys
import Adafruit_DHT
import picamera

# -----------------------------------DHT22---------------------------------
# Parse command line parameters.
sensor = Adafruit_DHT.DHT22
pin = 9

# Try to grab a sensor reading.  Use the read_retry method which will retry up
# to 15 times to get a sensor reading (waiting 2 seconds between each retry).
humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

# Un-comment the line below to convert the temperature to Fahrenheit.
# temperature = temperature * 9/5.0 + 32

# Note that sometimes you won't get a reading and
# the results will be null (because Linux can't
# guarantee the timing of calls to read the sensor).
# If this happens try again!
if humidity is not None and temperature is not None:
    print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
else:
    print('Failed to get reading. Try again!')
    sys.exit(1)
    
#-----------------------------IR sensor-------------------------
# Use BCM GPIO references
# instead of physical pin numbers
GPIO.setmode(GPIO.BCM)

#IR sensor setting
# Define GPIO to use on Pi
GPIO_PIR = 23

# Set pin as input
GPIO.setup(GPIO_PIR,GPIO.IN)

Current_State = GPIO.input(GPIO_PIR)
if Current_State ==1:
    print ("A remider: the window is not closed")
else:
    print ("Good job! THhe window is closed")
    
#-----------------------------Camera-----------------------------
camera = picamera.PiCamera()

#rotate 180 degrees if the picture is upside-down
#camera.rotation()

#change the resolution of the image; need frame rate 15 to enable the resolution
#camera.resolution = (2592,1944)
#camera.framerate = 15

#preview :use alpha=200 to adjust see-through
camera.start_preview(alpha=100)
camera.annotate_background = picamera.Color("blue")
camera.annotate_foreground = picamera.Color("yellow")
camera.annotate_text = "Hello world"
camera.annotate_text_size = 50 # the default size is 32
#time.sleep gives camera to sense the light
time.sleep(3)
#capture a picture
camera.capture('test.jpg')

camera.stop_preview()

#add a loop to take several pictures
#for i in range(2):
    #time.sleep(3)
    #capture a picture
    #camera.capture('test200.jpg')
    #camera.capture('test%s.jpg' %i)