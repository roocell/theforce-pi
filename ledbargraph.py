#!/usr/bin/env python3
#############################################################################
# Filename    : LightWater02.py
# Description : Control LED with 74HC595
# Author      : www.freenove.com
# modification: 2019/12/27
########################################################################
import RPi.GPIO as GPIO
import time
# Defines the data bit that is transmitted preferentially in the shiftOut function.
LSBFIRST = 1
MSBFIRST = 2
# define the pins for 74HC595
dataPin   = 16   #GPIO23   # DS Pin of 74HC595(Pin14)
latchPin  = 18   #GPIO24   # ST_CP Pin of 74HC595(Pin12)
clockPin = 22    #GPIO25   # CH_CP Pin of 74HC595(Pin11)

# the shift register only support 8 outputs
# so we'll control the last 2 directly with raspi GPIO
bar9Pin =  37 #GPIO25
bar10Pin = 35 #GPIO19

def setup():
    GPIO.setmode(GPIO.BOARD)    # use PHYSICAL GPIO Numbering
    GPIO.setup(dataPin, GPIO.OUT) # set pin to OUTPUT mode
    GPIO.setup(latchPin, GPIO.OUT)
    GPIO.setup(clockPin, GPIO.OUT)
    GPIO.setup(bar9Pin, GPIO.OUT)
    GPIO.setup(bar10Pin, GPIO.OUT)

# shiftOut function, use bit serial transmission.
def shiftOut(dPin,cPin,order,val):
    for i in range(0,8):
        GPIO.output(cPin,GPIO.LOW)
        if(order == LSBFIRST):
            GPIO.output(dPin,(0x01&(val>>i)==0x01) and GPIO.HIGH or GPIO.LOW)
        elif(order == MSBFIRST):
            GPIO.output(dPin,(0x80&(val<<i)==0x80) and GPIO.HIGH or GPIO.LOW)
        GPIO.output(cPin,GPIO.HIGH)

def display(value):
    if value < 8:
        x = 0x01
        x = x << value
        GPIO.output(latchPin,GPIO.LOW)  # Output low level to latchPin
        shiftOut(dataPin,clockPin,LSBFIRST,x) # Send serial data to 74HC595
        GPIO.output(latchPin,GPIO.HIGH) # Output high level to latchPin, and 74HC595 will update the data to the parallel output port.
        GPIO.output(bar9Pin,GPIO.LOW)
        GPIO.output(bar10Pin,GPIO.LOW)
    else:
        GPIO.output(latchPin,GPIO.LOW)  # Output low level to latchPin
        shiftOut(dataPin,clockPin,LSBFIRST,0x00) # Send serial data to 74HC595
        GPIO.output(latchPin,GPIO.HIGH) # Output high level to latchPin, and 74HC595 will update the data to the parallel output port.
        if value == 8:
            GPIO.output(bar9Pin,GPIO.HIGH)
            GPIO.output(bar10Pin,GPIO.LOW)
        else:
             # 10 or greater
            GPIO.output(bar9Pin,GPIO.LOW)
            GPIO.output(bar10Pin,GPIO.HIGH)

def loop():
    while True:
        x=0x01
        for i in range(0,8):
            GPIO.output(latchPin,GPIO.LOW)  # Output low level to latchPin
            shiftOut(dataPin,clockPin,LSBFIRST,x) # Send serial data to 74HC595
            GPIO.output(latchPin,GPIO.HIGH) # Output high level to latchPin, and 74HC595 will update the data to the parallel output port.
            x<<=1 # make the variable move one bit to left once, then the bright LED move one step to the left once.
            time.sleep(0.1)
        x=0x80
        for i in range(0,8):
            GPIO.output(latchPin,GPIO.LOW)
            shiftOut(dataPin,clockPin,LSBFIRST,x)
            GPIO.output(latchPin,GPIO.HIGH)
            x>>=1
            time.sleep(0.1)

def destroy():
    GPIO.cleanup()

if __name__ == '__main__': # Program entrance
    print ('Program is starting...' )
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        destroy()
