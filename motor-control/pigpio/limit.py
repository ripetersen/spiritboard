#!/usr/bin/env python3

#import RPi.GPIO as GPIO
import pigpio
import math
import time
MAX_PULSES=5000

directionX=26
stepX=19
directionY=13
stepY=6

us = 1000000

limit_hit = False

limitX=5
limits = {
        5: 'x-max',
        6: 'x-min',
        7: 'y-max',
        8: 'y-min'
}

pi = pigpio.pi()

def limit_callback(gpio, level, tick):
    global limit_hit
    limit_hit = True
    print("limit_hit(%d, %d, %d)" % (gpio, level, tick))
    pi.wave_tx_stop()

pi.callback(limitX, pigpio.EITHER_EDGE, limit_callback)
# Exports pin to userspace
print("x-axis direction : %02d"%directionX)
print("x-axis step      : %02d"%stepX)
print("x-axis limit     : %02d"%limitX)
print("y-axis direction : %02d"%directionY)
print("y-axis step      : %02d"%stepY)

while True:
    print('.')
    time.sleep(1)
pi.stop()


