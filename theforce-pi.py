#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
import ultrasonic
import ledbargraph
import segmentdisplay

def loop():
    while True:
        distance = ultrasonic.getSonar() # get distance
        print ("The distance is : %.2f cm"%(distance))

        for i in range(0,len(segmentdisplay.num)):
            segmentdisplay.display(i)
            time.sleep(0.5)

        x=0x01
        for i in range(0,8):
            ledbargraph.display(x)
            x<<=1 # make the variable move one bit to left once, then the bright LED move one step to the left once.
            time.sleep(0.1)
        x=0x80
        for i in range(0,8):
            ledbargraph.display(x)
            x>>=1
            time.sleep(0.1)

def setup():
    segmentdisplay.setup()
    ledbargraph.setup()
    ultrasonic.setup()

def destroy():
    GPIO.cleanup()

if __name__ == '__main__': # Program entrance
    print ('Program is starting...' )
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        destroy()
