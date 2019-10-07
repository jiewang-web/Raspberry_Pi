import RPi.GPIO as GPIO
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
import logging
import time
import json
import sys

# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO_PIR = 23
GPIO.setup(GPIO_PIR,GPIO.IN)
deviceShadowHandler = None

def customShadowCallback_upate(payload, responseStatus, token):
    # payload is a JSON string which will be parsed by jason lib
    if responseStatus == "timeout":
        print("Update request with " + token + " time out!")
    if responseStatus == "accepted":
        playloadDict = json.loads(payload)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print(payload)
        print("Update request with token: " + token + " accepted!")
        print("IR: " + str(playloadDict["state"]["reported"]["IR"]))
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n")
    if responseStatus == "rejected":
        print("Update request " + token + " rejected!")

def IR_state():
    Current_State = GPIO.input(GPIO_PIR)
    if Current_State == 1:
        rt = "A remider: the window is not closed"
    else:
        rt = "Good job! The window is closed"
    return rt

def sendCurrentState2AWSIoT():
    #check current status of device
    result = IR_state()
    print("Sending reported status to MQTT...")
    jsonPayload = '{"state":{"reported":{"IR":"' + result + '"}}}'
    print("Payload is: " + jsonPayload + "\n")
    deviceShadowHandler.shadowUpdate(jsonPayload, customShadowCallback_upate, 50)

def printDeviceStatus():
    print("=========================")
    status = IR_state()
    print(" Current status: " + str(status))
    print("=========================\n\n")

# Cofigure logging
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

awsiotHost = "a130ba174k0fld-ats.iot.us-west-2.amazonaws.com"
awsiotPort = 8883;
rootCAPath = "/home/pi/my_rpi/VeriSign-Class3-Public-Primary-Certification-Authority-G5.pem"
privateKeyPath = "/home/pi/my_rpi/78755df119-private.pem.key"
certificatePath = "/home/pi/my_rpi/78755df119-certificate.pem.crt"
myAWSIoTMQTTShadowClient = None;
myAWSIoTMQTTShadowClient = AWSIoTMQTTShadowClient("RPI_RULE")
myAWSIoTMQTTShadowClient.configureEndpoint(awsiotHost, awsiotPort)
myAWSIoTMQTTShadowClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

myAWSIoTMQTTShadowClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTShadowClient.configureConnectDisconnectTimeout(10) # 10sec
myAWSIoTMQTTShadowClient.configureMQTTOperationTimeout(10) #5sec

#connect to AWS IoT
myAWSIoTMQTTShadowClient.connect()

while True:
    #create a devcie Shadow with persistent subscription
    thingName = "my_rpi"
    deviceShadowHandler = myAWSIoTMQTTShadowClient.createShadowHandlerWithName(thingName, True)
    
    #print the intital status
    printDeviceStatus()
    
    #send initial status to IoT service
    sendCurrentState2AWSIoT()
    time.sleep(3)