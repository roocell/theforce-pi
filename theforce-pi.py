#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
import ultrasonic
import ledbargraph
import segmentdisplay

def loop():
    t=time.time()
    bavg = [0,0,0,0,0,0,0,0,0,0]
    bcnt = 0
    while True:
        distance = ultrasonic.getSonar() # get distance

        # divide into 8 segments of ultrasonic range to put into bargraph
        # detection only works reliably to like 50..70cm max
        b = int(distance*8.0/50.0)

        # moving average to stabilize it a bit
        bavg[bcnt]=b
        bcnt += 1
        if bcnt >= len(bavg):
            bcnt = 0
        b = int(sum(bavg)/len(bavg))

        ledbargraph.display(b)

        dt = time.time() - t
        if dt > 1:
            t = time.time()
            print ("The distance is : {} cm b {}".format(distance,b))

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
