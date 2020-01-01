#!/usr/bin/env python
# coding=utf-8

import RPi.GPIO as pi
import time

R, G = 5, 6
pi.setwarnings(False)

pi.setmode(pi.BCM)
pi.setup(R, pi.OUT)
pi.setup(G, pi.OUT)

pwmR = pi.PWM(R, 70)
pwmG = pi.PWM(G, 70)

pwmR.start(0)
pwmG.start(0)

try:
    t = 0.01
    while True:
        for i in range(0, 71):
            pwmR.ChangeDutyCycle(70)
            pwmG.ChangeDutyCycle(70 - i)
            time.sleep(t)
        for i in range(70, -1, -1):
            pwmR.ChangeDutyCycle(0)
            pwmG.ChangeDutyCycle(70 - i)
            time.sleep(t)
except KeyboardInterrupt:
    print("catch error")

pwmG.stop()
pwmR.stop()
pi.cleanup()
