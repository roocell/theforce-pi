#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

LSBFIRST = 1
MSBFIRST = 2
# define the pins for 74HC595
dataPin   = 11     #GPIO17 # DS Pin of 74HC595(Pin14)
latchPin  = 13     #GPIO27 # ST_CP Pin of 74HC595(Pin12)
clockPin = 15      #GPIO22 # CH_CP Pin of 74HC595(Pin11)

barDataPin   = 16   #GPIO23   # DS Pin of 74HC595(Pin14)
barLatchPin  = 18   #GPIO24   # ST_CP Pin of 74HC595(Pin12)
barClockPin = 22    #GPIO25   # CH_CP Pin of 74HC595(Pin11)


# SevenSegmentDisplay display the character "0"- "F" successively
num = [0xc0,0xf9,0xa4,0xb0,0x99,0x92,0x82,0xf8,0x80,0x90,0x88,0x83,0xc6,0xa1,0x86,0x8e]
def setup():
    GPIO.setmode(GPIO.BOARD)   # use PHYSICAL GPIO Numbering
    GPIO.setup(dataPin, GPIO.OUT)
    GPIO.setup(latchPin, GPIO.OUT)
    GPIO.setup(clockPin, GPIO.OUT)
    GPIO.setup(barDataPin, GPIO.OUT) # set pin to OUTPUT mode
    GPIO.setup(barLatchPin, GPIO.OUT)
    GPIO.setup(barClockPin, GPIO.OUT)

def shiftOut(dPin,cPin,order,val):
    for i in range(0,8):
        GPIO.output(cPin,GPIO.LOW);
        if(order == LSBFIRST):
            GPIO.output(dPin,(0x01&(val>>i)==0x01) and GPIO.HIGH or GPIO.LOW)
        elif(order == MSBFIRST):
            GPIO.output(dPin,(0x80&(val<<i)==0x80) and GPIO.HIGH or GPIO.LOW)
        GPIO.output(cPin,GPIO.HIGH);

def loop():
    while True:
        for i in range(0,len(num)):
            GPIO.output(latchPin,GPIO.LOW)
            shiftOut(dataPin,clockPin,MSBFIRST,num[i])  # Send serial data to 74HC595
            GPIO.output(latchPin,GPIO.HIGH)
            time.sleep(0.5)
        for i in range(0,len(num)):
            GPIO.output(latchPin,GPIO.LOW)
            shiftOut(dataPin,clockPin,MSBFIRST,num[i]&0x7f) # Use "&0x7f" to display the decimal point.
            GPIO.output(latchPin,GPIO.HIGH)
            time.sleep(0.5)

        # led bar graph
        x=0x01
        for i in range(0,8):
            GPIO.output(barLatchPin,GPIO.LOW)  # Output low level to latchPin
            shiftOut(barDataPin,barClockPin,LSBFIRST,x) # Send serial data to 74HC595
            GPIO.output(barLatchPin,GPIO.HIGH) # Output high level to latchPin, and 74HC595 will update the data to the parallel output port.
            x<<=1 # make the variable move one bit to left once, then the bright LED move one step to the left once.
            time.sleep(0.1)
        x=0x80
        for i in range(0,8):
            GPIO.output(barLatchPin,GPIO.LOW)
            shiftOut(barDataPin,barClockPin,LSBFIRST,x)
            GPIO.output(barLatchPin,GPIO.HIGH)
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
