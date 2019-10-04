#from picamera import PiCamera
import picamera 
import time

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