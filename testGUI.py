#!/usr/bin/python
# Filename: sensor.py
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
import AWSIoTPythonSDK
import logging
import time
import datetime
import face_recognition as fr
import RPi.GPIO as GPIO
import sys
import json
import requests
import picamera
import numpy as np
import testAPIs
import tkinter.font as tkFont
import tkinter as tk
import queue
import _thread
import os
from SNS_service import AWS_RPI_SNS

t = None
request_queue = queue.Queue()
result_queue = queue.Queue()


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
        self.rootCAPath = "/home/pi/Mirror/cerf/VeriSign-Class3-Public-Primary-Certification-Authority-G5.pem"
        self.privateKeyPath = "/home/pi/Mirror/cerf/78755df119-private.pem.key"
        self.certificatePath = "/home/pi/Mirror/cerf/78755df119-certificate.pem.crt"

        self.myAWSIoTMQTTShadowClient = AWSIoTMQTTShadowClient("RPI_RULE")
        self.myAWSIoTMQTTShadowClient.configureEndpoint(self.awsiotHost, self.awsiotPort)
        self.myAWSIoTMQTTShadowClient.configureCredentials(self.rootCAPath, self.privateKeyPath, self.certificatePath)

        self.myAWSIoTMQTTShadowClient.configureAutoReconnectBackoffTime(1, 32, 10)
        self.myAWSIoTMQTTShadowClient.configureConnectDisconnectTimeout(10) # 10sec
        self.myAWSIoTMQTTShadowClient.configureMQTTOperationTimeout(5) #5sec
        self.myAWSIoTMQTTShadowClient._AWSIoTMQTTClient.configureOfflinePublishQueueing(5, AWSIoTPythonSDK.core.util.enums.DropBehaviorTypes.DROP_OLDEST)  # Infinite offline Publish queueing
        #connect to AWS IoT
        self.myAWSIoTMQTTShadowClient.connect()

        #create a devcie Shadow with persistent subscription
        self.thingName = "my_rpi"
        self.deviceShadowHandler = self.myAWSIoTMQTTShadowClient.createShadowHandlerWithName(self.thingName, True)
        self.temperature = ""
        self.humidity = ""
        self.window = "True"
        self.human_presence = "True"

    def myShadowCallback_get(self, payload, responseStatus, token):
        # payload is a JSON string which will be parsed by jason lib
        print("into myShadowCallback_get")
        if (responseStatus == "timeout"):
            return 0
        if (responseStatus == "accepted"):
            payloadDict = json.loads(payload)
            self.temperature = payloadDict["state"]["reported"]["temperature"]
            self.humidity = payloadDict["state"]["reported"]["humidity"]
            self.window = payloadDict["state"]["reported"]["window_is_open"]
            self.human_presence = payloadDict["state"]["reported"]["people_at_home"]

        if (responseStatus == "rejected"):
            return -1

    def myShadowGet(self, timeout=5):
        print("into myShadowGet")
        self.deviceShadowHandler.shadowGet(self.myShadowCallback_get, timeout)
        
class MirrorBody:
    def __init__(self, hum=-1, temp=-1, isW=-1, fm="", fd=""):
        self.temperature = temp
        self.humidity = hum
        self.isWindowOpen = isW
        self.forecast_main = fm
        self.forecast_desc = fd
        self.hp_instance = ""
        self.forecast_temp = "";
        

    def self_check(self):
        init_success = False
        while not init_success:
            init_success = True
        return init_success


    def getAll(self):
        # ForeCast
        response = requests.get(testAPIs.weatherurlbuilder())
        response = json.loads(response.text)
        self.forecast_main = response["list"][0]["weather"][0]["main"]
        self.forecast_desc = response["list"][0]["weather"][0]["description"]
        self.forecast_temp = "{:.2f}".format(response["list"][0]["main"]["temp"]-273.15)

    def getPic(self,camera):
        camera.capture(output, format="rgb")
        return output
    
    def getHumanPresence(self):
        return this.hp_instance.decision()


def submit_to_tkinter(callable, *args, **kwargs):
    request_queue.put((callable, args, kwargs))
    return result_queue.get()


def threadmain():
    global t

    def timertick():
        try:
            callable, args, kwargs = request_queue.get_nowait()
        except queue.Empty:
            pass
        else:
            retval = callable(*args, **kwargs)
            result_queue.put(retval)

        t.after(500, timertick)

    t = tk.Tk()
    t.overrideredirect(1)
    t.configure(background='black')
    ft1 = tkFont.Font(size=24, weight=tkFont.BOLD)
    w = t.winfo_screenwidth()
    h = t.winfo_screenheight()
    t.geometry("%dx%d" % (w, h))
    mr = MirrorBody()
    mr.getAll()
    forecast_weather_label = tk.Label(name="fw", text=str(mr.forecast_desc), bg="black", fg="white", font=ft1)
    forecast_weather_label.grid(row=0,column=0,padx=0.15*w)
    forecast_temp_label = tk.Label(name="ft",text=str(mr.forecast_temp)+"°C", bg="black", fg="white", font=ft1)
    forecast_temp_label.grid(row=1,column=0)
    name_label = tk.Label(name="nl",text="Hi!", bg="black", fg="white", font=ft1)
    name_label.grid(row=0,column=1,padx=0.15*w)
    date_label = tk.Label(name="dl",text=str(datetime.date.today()), bg="black", fg="white", font=ft1)
    date_label.grid(row=0, column=2, sticky=tk.N+tk.E)
    
    place_holder0 = tk.Label(text="", bg="black", fg="white", font=ft1)
    place_holder0.grid(row=2,column=0)
    place_holder1 = tk.Label(text="", bg="black", fg="white", font=ft1)
    place_holder1.grid(row=3,column=0)
    place_holder2 = tk.Label(text="", bg="black", fg="white", font=ft1)
    place_holder2.grid(row=4,column=0)
    
    time_holder = tk.Label(name="time", text=str(time.strftime("%H:%M", time.localtime())), bg="black", fg="white", font=ft1)
    time_holder.grid(row=1,column=2)
    
    room_label = tk.Label(text="Indoor °C/%", bg="black", fg="white", font=ft1)
    room_label.grid(row=5,column=0)
    room_details_label = tk.Label(name="indoor",text="-1°C/-1%", bg="black", fg="white", font=ft1)
    room_details_label.grid(row=6,column=0)
    timertick()
    t.mainloop()


def update_recog(match_name):
    name_str = "Hi "
    for match in match_name:
        name_str += (str(match)+",")
    t.nametowidget(".nl").configure(text=name_str)

def update(mr, ar):
    t.nametowidget(".time").configure(text=str(time.strftime("%H:%M", time.localtime())))
    t.nametowidget(".fw").configure(text=str(mr.forecast_desc))
    t.nametowidget(".ft").configure(text=str(mr.forecast_temp)+"°C")
    t.nametowidget(".indoor").configure(text=str(ar.temperature)+"°C/"+str(ar.humidity)+"%")


if __name__ == '__main__':
    known_enconding = []
    namelist = []
    for filename in os.listdir(r"./known_pictures"):
        face_read = fr.load_image_file("known_pictures/"+filename)
        face_encode = fr.face_encodings(face_read)[0]
        face_name = filename.split(".jpg")[0]
        known_enconding.append(face_encode)
        namelist.append(face_name)
    camera = picamera.PiCamera()
    camera.resolution = (320, 240)
    output = np.empty((240, 320, 3), dtype=np.uint8)
    mr = MirrorBody()
    init_success = mr.self_check
    while not init_success:
        init_success = mr.self_check
    mr.getAll()
    ar = AWS_RPI()
    sns_ins = AWS_RPI_SNS()
    _thread.start_new_thread(threadmain, ())
    trigger = 0
    while 1:
        trigger += 1
        trigger = trigger % 8
        if trigger == 0:
            mr.getAll()
            ar.myShadowGet()
            

        if trigger == 3:
            match_name = []
            output = mr.getPic(camera)
            face_locations = fr.face_locations(output)
            face_encodings = fr.face_encodings(output, face_locations)
            for face_encoding in face_encodings:
                match = fr.compare_faces(known_enconding, face_encoding)
                for i, res in enumerate(match):
                    if match[i]:
                        match_name.append(namelist[i])
            print(match_name)
            face_v = "False"
            if match_name:
                face_v = "True"
            sns_ins.data_sns_upload(ar.window, ar.human_presence, face_v)
            submit_to_tkinter(update_recog, match_name)
        if trigger == 5:
            sns_ins.send2AWS()
            submit_to_tkinter(update, mr, ar)

        time.sleep(2)