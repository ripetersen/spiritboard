#!/usr/bin/env python3

#import RPi.GPIO as GPIO
import pigpio
import math
import time

directionX=26
stepX=19
directionY=13
stepY=6

us = 1000000

limitX=5
limits = {
        5: 'x-max',
        6: 'x-min',
        7: 'y-max',
        8: 'y-min'
}

pi = pigpio.pi()


# Exports pin to userspace
print("x-axis direction : %02d"%directionX)
print("x-axis step      : %02d"%stepX)
print("x-axis limit     : %02d"%limitX)
print("y-axis direction : %02d"%directionY)
print("y-axis step      : %02d"%stepY)

pi.write(directionX,0)
pi.write(directionY,0)

microsteps=16
steps=200
steps_per_revolution = steps * microsteps

x_steps=[]
y_steps=[]

t = 1
x_steps = [
        pigpio.pulse(1<<stepX, 0, math.ceil((t*us)/(2*steps_per_revolution))),
        pigpio.pulse(0, 1<<stepX, math.ceil((t*us)/(2*steps_per_revolution)))
] 
pi.wave_clear()
pulse_count = pi.wave_add_generic(x_steps)
xWave = pi.wave_create()
print("x wave")
print("pulse count %d" % pulse_count)
print("wave micros %d" % pi.wave_get_micros())
t = 2
y_steps = [
        pigpio.pulse(1<<stepY, 0, math.ceil((t*us)/(2*steps_per_revolution))),
        pigpio.pulse(0, 1<<stepY, math.ceil((t*us)/(2*steps_per_revolution)))
]
pulse_count = pi.wave_add_generic(y_steps)
yWave = pi.wave_create()
print("y wave")
print("pulse count %d" % pulse_count)
print("wave micros %d" % pi.wave_get_micros())
#pi.wave_send_once(xWave)
#
start = time.time()
pi.wave_chain([
    255, 0,
    xWave, yWave, 
    255, 1, steps_per_revolution % 255, steps_per_revolution // 255
    ])
print(time.time() - start)
while pi.wave_tx_busy():
    pass
print(time.time() - start)

pi.stop()


