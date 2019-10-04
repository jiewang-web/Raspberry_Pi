import RPi.GPIO as GPIO
import time
import sys

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