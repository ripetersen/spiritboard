#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time
import sys

GPIO.cleanup()

GPIO.setmode(GPIO.BCM)

limitX=5
stop=False

GPIO.setup(limitX, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def my_callback(channel):  
    global stop
    stop=True
    print("limit detected on %0d"%limitX) 

GPIO.add_event_detect(limitX, GPIO.FALLING, callback=my_callback, bouncetime=300) 

while True:
    print(stop)
    time.sleep(1)


