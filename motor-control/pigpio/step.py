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
    print("limit_hit")
    pi.wave_tx_stop()

pi.callback(limitX, pigpio.RISING_EDGE, limit_callback)
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

def makeWaves(fast, fastGPIO, slow, slowGPIO, delay):
    delay = max(50, math.ceil(delay/2))
    if slow == 0:
        slow = fast
        slowGPIO = fastGPIO
        fast = 0
        fastGPIO = slowGPIO
    waves = gcd(fast, slow)
    slow = slow // waves
    fast = fast // waves
    slope = fast/slow
    pulses = []
    total_pulses = 0
    for i in range(slow):
        needed_pulses = round((i+1)*slope) - total_pulses
        if needed_pulses > 0:
            pulses.append(pigpio.pulse(1<<fastGPIO | 1<<slowGPIO, 0, delay))
            pulses.append(pigpio.pulse(0, 1<<fastGPIO | 1<<slowGPIO, delay))
            pulses.extend((needed_pulses - 1) * [pigpio.pulse(1<<fastGPIO, 0, delay), pigpio.pulse(0, 1<<fastGPIO, delay)])
            total_pulses += needed_pulses
        else:
            # TODO: will this ever happen?
            pulses.append(pigpio.pulse(1<<slowGPIO, 0, delay))
            pulses.append(pigpio.pulse(0, 1<<slowGPIO, delay))
    if fast > total_pulses:
            needed_pulses = fast-total_pulses
            pulse.extend(needed_pulses * [pigpio.pulse(1<<fastGPIO, 0, delay), pigpio.pulse(0, 1<<fastGPIO, delay)])
            total_pulses += needed_pulses
    if total_pulses != fast:
        print("Expected total_pulses to equal fast : %d <> %d"%(total_pulses, fast))

    print("%d pulses" % len(pulses))
    print("%d loops" % waves)
    while len(pulses) > 0:
        if limit_hit:
            break
        total_loops = waves
        while total_loops > 0:
            while pi.wave_tx_busy():
                pass
            pi.wave_clear()
            pi.wave_add_generic(pulses[:MAX_PULSES])
            wave = pi.wave_create()
            loops = min(total_loops, 65535)
            if limit_hit:
                break
            print('sending chain')
            pi.wave_chain([
                255, 0,
                    wave,
                255, 1, loops % 256, loops // 256
            ])
            total_loops -= loops
        pulses = pulses[MAX_PULSES:]

def gcd(a, b):
    if b==0:
        return a
    return gcd(b, a%b)

def move(x, y, t):
    print("move(%d, %d, %d)"%(x,y,t))

    if x > y:
        delay = (t*us)/x
        makeWaves(x, stepX, y, stepY, delay)
    else:
        delay = (t*us)/y
        makeWaves(y, stepY, x, stepX, delay)


#print()
#move(steps_per_revolution, 2*steps_per_revolution, 1)
#print()
#move(steps_per_revolution, math.floor(2.1*steps_per_revolution), 1)
print()
#print(gcd(3000, 5000))
#move(3000, 5000, 1)
#move(4*steps_per_revolution, 4*steps_per_revolution, 0.5)
start = time.time()
move(steps_per_revolution, 5 * steps_per_revolution, 2.5)
while pi.wave_tx_busy():
    pass
print(time.time() - start)


#t = 2
#y_steps = [
#        pigpio.pulse(1<<stepY, 0, math.ceil((t*us)/(2*steps_per_revolution))),
#        pigpio.pulse(0, 1<<stepY, math.ceil((t*us)/(2*steps_per_revolution)))
#]
#pulse_count = pi.wave_add_generic(y_steps)
#yWave = pi.wave_create()
#print("y wave")
#print("pulse count %d" % pulse_count)
#print("wave micros %d" % pi.wave_get_micros())
#pi.wave_send_once(xWave)
#
#start = time.time()
#print(time.time() - start)
#while pi.wave_tx_busy():
#    pass
#print(time.time() - start)

pi.stop()


