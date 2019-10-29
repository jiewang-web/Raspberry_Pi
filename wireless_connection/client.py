#!/usr/bin/env python
import socket
import time
import ultra_fun
from DHT22_fun import DHT

TCP_IP = '192.168.1.17'#'127.27.180.36'#
TCP_PORT = 6677
BUFFER_SIZE = 1024
# MESSAGE: ultrasonic_sensor
d = 10
MESSAGE0 = ultra_fun.distance()
while (d > 1):
    MESSAGE1 = ultra_fun.distance()
    d = abs(MESSAGE1 - MESSAGE0)
    MESSAGE0 = MESSAGE1
#MESSAGE: DHT22
MESSAGE2 = DHT()
temper = MESSAGE2[0]
humidity = MESSAGE2[1]

MESSAGE = (str(MESSAGE0) + '\n' + str(humidity) + '\n' + str(temper)) #+ str(MESSAGE2) #

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
time.sleep(2)
s.send(MESSAGE)
data = s.recv(BUFFER_SIZE)
s.close()

print ("received data:", data)