#Libraries
import RPi.GPIO as GPIO
import time

def distance():
    #GPIO Mode (BOARD / BCM)
    GPIO.setmode(GPIO.BCM)
     
    #set GPIO Pins
    GPIO_TRIGGER = 24
    GPIO_ECHO = 23
     
    #set GPIO direction (IN / OUT)
    GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
    GPIO.setup(GPIO_ECHO, GPIO.IN)
    try:
        while True:
            # set Trigger to HIGH
            GPIO.output(GPIO_TRIGGER, True)
 
            # set Trigger after 0.01ms to LOW
            time.sleep(0.00001)
            GPIO.output(GPIO_TRIGGER, False)
 
            StartTime = time.time()
            StopTime = time.time()
 
            # save StartTime
            while GPIO.input(GPIO_ECHO) == 0:
                StartTime = time.time()
 
            # save time of arrival
            while GPIO.input(GPIO_ECHO) == 1:
                StopTime = time.time()
 
            # time difference between start and arrival
            TimeElapsed = StopTime - StartTime
            # multiply with the sonic speed (34300 cm/s)
            # and divide by 2, because there and back
            distance = (TimeElapsed * 34300) / 2
            distance = round(distance, 2)
            print ("Measured Distance = %.1f cm" % distance)
            time.sleep(1)
 
            return distance
        
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
    
            
            
            
            