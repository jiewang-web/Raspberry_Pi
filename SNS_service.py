from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
import AWSIoTPythonSDK
import logging
import time
import json
import sys


class AWS_RPI_SNS:
    def __init__(self):

        # Cofigure logging
        self.logger = logging.getLogger("AWSIoTPythonSDK.core")
        self.logger.setLevel(logging.DEBUG)
        self.streamHandler = logging.StreamHandler()
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.streamHandler.setFormatter(self.formatter)
        self.logger.addHandler(self.streamHandler)

        self.awsiotHost = "a130ba174k0fld-ats.iot.us-west-2.amazonaws.com"
        self.awsiotPort = 8883
        self.rootCAPath = "/home/pi/Mirror/VeriSign-Class3-Public-Primary-Certification-Authority-G5.pem"
        self.privateKeyPath = "/home/pi/Mirror/f31485c816-private.pem.key"
        self.certificatePath = "/home/pi/Mirror/f31485c816-certificate.pem.crt"

        self.myAWSIoTMQTTShadowClient = AWSIoTMQTTShadowClient("RPI_RULE")
        self.myAWSIoTMQTTShadowClient.configureEndpoint(self.awsiotHost, self.awsiotPort)
        self.myAWSIoTMQTTShadowClient.configureCredentials(self.rootCAPath, self.privateKeyPath, self.certificatePath)

        self.myAWSIoTMQTTShadowClient.configureAutoReconnectBackoffTime(1, 32, 20)
        self.myAWSIoTMQTTShadowClient.configureConnectDisconnectTimeout(10) # 10sec
        self.myAWSIoTMQTTShadowClient.configureMQTTOperationTimeout(10) #5sec
        self.myAWSIoTMQTTShadowClient._AWSIoTMQTTClient.configureOfflinePublishQueueing(5, AWSIoTPythonSDK.core.util.enums.DropBehaviorTypes.DROP_OLDEST)
        
        #connect to AWS IoT
        self.myAWSIoTMQTTShadowClient.connect()

        #create a devcie Shadow with persistent subscription
        self.thingName = "SNS_service"
        self.deviceShadowHandler = self.myAWSIoTMQTTShadowClient.createShadowHandlerWithName(self.thingName, True)
        self.window_status = "False"
        self.people_status = "True"
        self.face_status = "False"

    def customShadowCallback_upate(self, payload, responseStatus, token):
        # payload is a JSON string which will be parsed by jason lib
        if (responseStatus == "timeout"):
            print("Update request with " + token + " time out!")
        if (responseStatus == "accepted"):
            playloadDict = json.loads(payload)
        if (responseStatus == "rejected"):
            print("Update request " + token + " rejected!")

    def data_sns_upload(self, window_v, presence_v, face_v):
        
        self.window_status = window_v
        self.people_status = presence_v
        self.face_status = face_v

    def customShadowCallback_delete(self, payload, responseStatus, token):
        if (responseStatus == "timeout"):
            raise(" time out!")
        if (responseStatus == "accepted"):
            print(" accepted!")
        if (responseStatus == "rejected"):
            raise(" rejected!")

    def send2AWS(self):
        # check current status of device
        window = self.window_status
        people = self.people_status
        face = self.face_status  
        jsonPayload = '{"state":{"reported":{ "window_is_open": "' + str(window) + '", "people_at_home": "' + str(people) + '", "face_recognition": "' + str(face) + '"}}}'
        
              
        if people == "False":
            if face == "False" or window == "True":
                self.deviceShadowHandler.shadowUpdate(jsonPayload, self.customShadowCallback_upate, 10)
            
        else:
            if face == "False":
                self.deviceShadowHandler.shadowUpdate(jsonPayload, self.customShadowCallback_upate, 10)


