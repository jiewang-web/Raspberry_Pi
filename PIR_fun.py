# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 12:42:44 2019
@author: SAM
"""
import time

import RPi.GPIO as GPIO

def decision():
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(26, GPIO.IN)         #Read output from PIR motion sensor

	for m in range(2):
		i = GPIO.input(26)
		time.sleep(2)
	return i
