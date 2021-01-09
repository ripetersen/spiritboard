#!/bin/bash

X_DIRECTION=26
X_STEP=19
Y_DIRECTION=13
Y_STEP=6
# Exports pin to userspace
echo "$X_DIRECTION"
echo "$X_STEP" 
echo "$Y_DIRECTION"
echo "$Y_STEP" 

read

if [ ! -d /sys/class/gpio/gpio${X_STEP}/ ]; then
	echo "exporting $X_STEP"
	echo "$X_STEP" > /sys/class/gpio/export                  
fi
if [ ! -d /sys/class/gpio/gpio${Y_STEP}/ ]; then
	echo "exporting $Y_STEP"
	echo "$Y_STEP" > /sys/class/gpio/export                  
fi
if [ ! -d /sys/class/gpio/gpio${X_DIRECTION}/ ]; then
	echo "exporting $X_DIRECTION"
	echo "$X_DIRECTION" > /sys/class/gpio/export                  
fi
if [ ! -d /sys/class/gpio/gpio${Y_DIRECTION}/ ]; then
	echo "exporting $Y_DIRECTION"
	echo "$Y_DIRECTION" > /sys/class/gpio/export                  
fi

read

# Sets pin 18 as an output
echo "out" > /sys/class/gpio/gpio${X_STEP}/direction
echo "out" > /sys/class/gpio/gpio${X_DIRECTION}/direction
echo "out" > /sys/class/gpio/gpio${Y_STEP}/direction
echo "out" > /sys/class/gpio/gpio${Y_DIRECTION}/direction

# Sets pin 18 to high
DIR=0
MICROSTEPS=16
STEPS=200
for r in $(seq 10); do
	echo $((r % 2)) > /sys/class/gpio/gpio${X_DIRECTION}/value
	echo $(( ! (r % 2))) > /sys/class/gpio/gpio${Y_DIRECTION}/value
	for s in $(seq $(($MICROSTEPS * $STEPS))); do
#		echo $s
		echo "1" > /sys/class/gpio/gpio${X_STEP}/value
		echo "1" > /sys/class/gpio/gpio${Y_STEP}/value
		# Sets pin 18 to low
		echo "0" > /sys/class/gpio/gpio${X_STEP}/value 
		echo "0" > /sys/class/gpio/gpio${Y_STEP}/value
	done
done 
