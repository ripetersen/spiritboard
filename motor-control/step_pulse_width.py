#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time

GPIO.cleanup()

GPIO.setmode(GPIO.BCM)

stop=False
limit_triggered=None

directionX=26
stepX=19
limitX=5
directionY=13
stepY=6
limits = {
        5: 'x-max',
        6: 'x-min',
        7: 'y-max',
        8: 'y-min'
}
# Exports pin to userspace
print("x-axis direction : %02d"%directionX)
print("x-axis step      : %02d"%stepX)
print("x-axis limit     : %02d"%limitX)
print("y-axis direction : %02d"%directionY)
print("y-axis step      : %02d"%stepY)

GPIO.setup(limitX, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def limit_hit(channel):  
    global stop, limit_triggered
    stop = True
    limit_triggered = channel
    print("limit detected on %0d"%channel) 

GPIO.add_event_detect(limitX, GPIO.FALLING, callback=limit_hit, bouncetime=300) 

GPIO.setup(directionX, GPIO.OUT)
GPIO.setup(stepX, GPIO.OUT)
GPIO.setup(directionY, GPIO.OUT)
GPIO.setup(stepY, GPIO.OUT)

# Sets pin 18 to high
dir=0
cycles=10
microsteps=16
steps=200
x_steps=0
y_steps=0
steps_per_revolution = steps * microsteps
for c in range(cycles):
    if stop:
        break
    GPIO.output(directionX, c%2)
    GPIO.output(directionY, (c+1)%2)
    period = (cycles - c)/10
    steps_per_second = steps_per_revolution / period
    print("======================")
    print("period = %0f"%period)
    print("rpm = %0f"%(60/period))
    pulse_width = period/steps_per_revolution
    print("pusle width = %fms"%(pulse_width*1000))
    start = time.time()

    for s in range(steps_per_revolution):
        if stop:
            break
        GPIO.output(stepX, 1)
        x_steps+=1
        GPIO.output(stepY, 1)
        y_steps+=1
        time.sleep(pulse_width/2)
        GPIO.output(stepX, 0)
        GPIO.output(stepY, 0)
        time.sleep(pulse_width/2)
    elapsed_time = time.time()-start
    print("elapsed time = %f"%(time.time()-start))
    print("actual rpm = %f"%(60/elapsed_time))
if limit_triggered:
    print('%s triggered'%limits[limit_triggered])
print("X steps: %d"%x_steps)
print("Y steps: %d"%y_steps)
