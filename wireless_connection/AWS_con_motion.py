from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
import AWSIoTPythonSDK
import logging
import time
import json
import sys
import PIR_fun


class AWS_RPI:
    def __init__(self):

        # Cofigure logging
        self.logger = logging.getLogger("AWSIoTPythonSDK.core")
        self.logger.setLevel(logging.DEBUG)
        self.streamHandler = logging.StreamHandler()
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.streamHandler.setFormatter(self.formatter)
        self.logger.addHandler(self.streamHandler)

        self.awsiotHost = "a130ba174k0fld-ats.iot.us-west-2.amazonaws.com"
        self.awsiotPort = 443
        self.rootCAPath = "/home/pi/my_rpi/VeriSign-Class3-Public-Primary-Certification-Authority-G5.pem"
        self.privateKeyPath = "/home/pi/my_rpi/78755df119-private.pem.key"
        self.certificatePath = "/home/pi/my_rpi/78755df119-certificate.pem.crt"

        self.myAWSIoTMQTTShadowClient = AWSIoTMQTTShadowClient("RPI_RULE")
        self.myAWSIoTMQTTShadowClient.configureEndpoint(self.awsiotHost, self.awsiotPort)
        self.myAWSIoTMQTTShadowClient.configureCredentials(self.rootCAPath, self.privateKeyPath, self.certificatePath)

        self.myAWSIoTMQTTShadowClient.configureAutoReconnectBackoffTime(1, 32, 20)
        self.myAWSIoTMQTTShadowClient.configureConnectDisconnectTimeout(10) # 10sec
        self.myAWSIoTMQTTShadowClient.configureMQTTOperationTimeout(10) #5sec
        self.myAWSIoTMQTTShadowClient._AWSIoTMQTTClient.configureOfflinePublishQueueing(2, AWSIoTPythonSDK.core.util.enums.DropBehaviorTypes.DROP_OLDEST)

        #connect to AWS IoT
        self.myAWSIoTMQTTShadowClient.connect()

        #create a devcie Shadow with persistent subscription
        self.thingName = "my_rpi"
        self.deviceShadowHandler = self.myAWSIoTMQTTShadowClient.createShadowHandlerWithName(self.thingName, True)


    def customShadowCallback_upate(self, payload, responseStatus, token):
        # payload is a JSON string which will be parsed by jason lib
        if (responseStatus == "timeout"):
            print("Update request with " + token + " time out!")
        if (responseStatus == "accepted"):
            playloadDict = json.loads(payload)
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print(payload)
            print("Update request with token: " + token + " accepted!")
            print("state: " + str(playloadDict["state"]["reported"]))
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n")
        if (responseStatus == "rejected"):
            print("Update request " + token + " rejected!")

    def data_upload(self):
        presence = True
        presence = PIR_fun.decision()

        return presence

    def customShadowCallback_delete(self, payload, responseStatus, token):
        if (responseStatus == "timeout"):
            print("Delete request " + token + " time out!")
        if (responseStatus == "accepted"):
            print("Delete request with token " + token + " accepted!")
        if (responseStatus == "rejected"):
            print("Delete request with token " + token + " rejected!")

    def send2AWS(self):
        # check current status of device
        p_presence = self.data_upload()
        if(p_presence == 0):
            p_presence = False
        else: 
            p_presence = True

        # print("Sending reported status to MQTT...")
        # jsonPayload = '{"state":{"reported":{"window status": "' + window  + "; humidity is: " + humidity + "; temperature is: " + temperature + "; face detection is: " + message + '"}}}'
        
        jsonPayload = '{"state":{"reported":{"people_at_home": "' + str(p_presence) + '"}}}'
        
        print("Payload is: " + jsonPayload + "\n")
        
        #Delete shadow JSON doc
        # self.deviceShadowHandler.shadowDelete(self.customShadowCallback_delete, 50)

        self.deviceShadowHandler.shadowUpdate(jsonPayload, self.customShadowCallback_upate, 10)

        print("=========================")
        # print(" Current status: " + str(window + '\n'+ humidity + temperature + face + presence))
        print("=========================\n\n")

    def myShadowCallback_get(self, payload, responseStatus, token):
        # payload is a JSON string which will be parsed by jason lib
        if (responseStatus == "timeout"):
            print("Update request with " + token + " time out!")
            return 0

        if (responseStatus == "accepted"):
            playloadDict = json.loads(payload)
            print(payload)
            return playloadDict

        if (responseStatus == "rejected"):
            return -1

    def myShadowGet(timeout=5):
        self.deviceShadowHandler.shadowGet(self.myShadowCallback_get, timeout)


if __name__ == "__main__":
    AR = AWS_RPI()

    #send unsual status to IoT service
    AR.send2AWS()#


