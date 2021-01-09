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

def one_wave():
    steps = [
            pigpio.pulse(1<<stepX | 1<<stepY, 0, 156),
            pigpio.pulse(1<<stepX,  1<<stepY   , 156),
            pigpio.pulse(1<<stepY,  1<<stepX   ,  156),
            pigpio.pulse(0, 1<<stepX |  1<<stepY , 156),
    ] 
    pi.wave_clear()
    pulse_count = pi.wave_add_generic(steps)
    wave = pi.wave_create()
    print("1 wave")
    print("pulse count %d" % pulse_count)
    print("wave micros %d" % pi.wave_get_micros())
    pi.wave_chain([
        255, 0,
        xWave, 
        255, 1, (steps_per_revolution) % 255, (steps_per_revolution) // 255
        ])

def makeWaves(fast, fastGPIO, slow, slowGPIO, delay):
    waves = gcd(fast, slow)
    slow = slow // waves
    fast = fast // waves
    slope = fast/slow
    pulses = []
    for s in range(slow):
        pulses.append(

    waves = min(slow, fast // slope)
    delay = math.ceil(delay/2)
    print("slope %d // %d = %d"%(fast,slow,slope))
    print("waves min(%d, %d // %d) = %d"%(slow, fast,slope,waves))

    pi.wave_clear()

    fastPulse = [
            pigpio.pulse(1<<fastGPIO, 0, delay ), 
            pigpio.pulse(0, 1<<fastGPIO, delay )]
    pi.wave_add_generic(fastPulse)
    fastWave = pi.wave_create()
    print("fastWave : %d" % fastWave)

    slowPulse = [
            pigpio.pulse(1<<slowGPIO, 0, delay ), 
            pigpio.pulse(0, 1<<slowGPIO, delay )]
    pi.wave_add_generic(slowPulse)
    slowWave = pi.wave_create()
    print("slowWave : %d" % slowWave)

    wave_commands = [
        255, 0,
            slowWave, 
            255, 0,
                fastWave,
            255, 1, slope % 255, slope // 255,
        255, 1, waves % 255, waves // 255
        ]
    slow_remainder = slow - waves
    print("slow_remainder %d"%slow_remainder)
    if slow_remainder>0 :
        wave_commands.extend([
            255, 0,
                slowWave,
            255, 1, slow_remainder % 255, slow_remainder // 255])
    fast_remainder = fast - (waves * slope)
    print("fast_remaindee %d"%fast_remainder)
    if fast_remainder>0 :
        wave_commands.extend([
            255, 0,
                fastWave,
            255, 1, fast_remainder % 255, fast_remainder // 255])
    pi.wave_chain(wave_commands)

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
print(gcd(3000, 5000))
#move(3000, 5000, 1)


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


