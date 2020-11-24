#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
import ultrasonic
import ledbargraph
import segmentdisplay
import servo

def loop():
    t=time.time()
    bavg = [0] * 100
    bcnt = 0
    lastb = -1
    lastbcnt = 0
    countdown = 9
    while True:
        distance = ultrasonic.getSonar() # get distance

        # divide into 10 segments of ultrasonic range to put into bargraph
        # detection only works reliably to like 50..70cm max
        b = int(distance*10.0/50.0)

        # moving average to stabilize it a bit
        bavg[bcnt]=b
        bcnt += 1
        if bcnt >= len(bavg):
            bcnt = 0
        b = int(sum(bavg)/len(bavg))

        ledbargraph.display(b)

        # per second operations
        dt = time.time() - t
        if dt > 1:
            t = time.time()

            # if we've stayed on the 4th bar (heh heh - May the 4th be with you.)
            # for 1 seconds. then start the countdown.
            if b == 3 and b == lastb:
                lastbcnt += 1
                if lastbcnt >= 1: # hold it for 1 second
                    # start countdown (b must remain the same though!)
                    segmentdisplay.display(countdown)
                    print("countdown {}".format(countdown))
                    countdown -= 1
                    if countdown < 0:
                        servo.servoWrite(90)
                        time.sleep(0.5)
                        servo.servoWrite(0)
                        countdown = 0 # so we dont display lower
            else:
                servo.off()
                lastbcnt = 0
                segmentdisplay.off()
                countdown = 9
            lastb = b

            print ("The distance is : {} cm b {}".format(distance,b))

def setup():
    segmentdisplay.setup()
    ledbargraph.setup()
    ultrasonic.setup()
    servo.setup()

def destroy():
    segmentdisplay.destroy()
    ledbargraph.destroy()
    ultrasonic.destroy()
    servo.destroy()

    GPIO.cleanup()

if __name__ == '__main__': # Program entrance
    print ('Program is starting...' )
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        destroy()
