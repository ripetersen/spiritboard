#!/usr/bin/env python3

import RPi.GPIO as GPIO
import math
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
cycles=1
microsteps=16
steps=200
x_steps=0
y_steps=0
steps_per_revolution = steps * microsteps
window = 0.1
for c in range(cycles):
    if stop:
        break
    GPIO.output(directionX, c%2)
    GPIO.output(directionY, (c+1)%2)
    total_time = 3 
    steps_remaining = 3*steps_per_revolution
    print("======================")
    print("time = %0f" % total_time)
    print("steps = %d" % steps_remaining)
    start_time = time.time()
    end_time = start_time + total_time
    window_elapsed = window
    while steps_remaining > 0:
        if stop:
            break
        # calculate the necessary pulse time
        time_remaining = end_time - time.time() 
        omega = 1.5 * steps_remaining/time_remaining if time_remaining > 0 else 10000
        print("steps remaining = %d"%steps_remaining)
#        print("time remaining = %f"%time_remaining)
        print("omega = %f steps/sec"%omega)
        f = 1/omega
        pulse = f/8
        window_elapsed = max(window, window_elapsed)
        print("window elapsed : %f"%window_elapsed)
        next_steps = min(steps_remaining, math.ceil(window_elapsed * omega))
        print("next_steps = %d"%next_steps)
        steps_remaining -= next_steps
        window_start = time.time()
        for s in range(next_steps):
            GPIO.output(stepX, 1)
            GPIO.output(stepY, 1)
            time.sleep(pulse)
            GPIO.output(stepX, 0)
            GPIO.output(stepY, 0)
            time.sleep(pulse)
        window_elapsed = time.time()-window_start
        print("actual omega : %f"%(next_steps/window_elapsed))
    elapsed_time = time.time()-start_time
    print("elapsed time = %f"%(time.time()-start_time))
if limit_triggered:
    print('%s triggered'%limits[limit_triggered])
print("X steps: %d"%x_steps)
print("Y steps: %d"%y_steps)
