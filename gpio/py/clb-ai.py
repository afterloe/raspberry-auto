#!/usr/bin/env python
# coding=utf-8

import RPi.GPIO as GPIO
import time

R, G = 5, 6
Buzzer = 17

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)
GPIO.setup(R, GPIO.OUT)
GPIO.setup(G, GPIO.OUT)
GPIO.setup(Buzzer, GPIO.OUT)

global Buzz
Buzz = GPIO.PWM(Buzzer, 440)
Buzz.start(50)

pwmR = GPIO.PWM(R, 70)
pwmG = GPIO.PWM(G, 70)

pwmR.start(0)
pwmG.start(0)

try:
    t = 0.01
    while True:
        for i in range(0, 71):
            pwmG.ChangeDutyCycle(70)
            Buzz.ChangeFrequency(500 - i)
            pwmR.ChangeDutyCycle(70 - i)
            print(i)
            time.sleep(t)
        for i in range(70, -1, -1):
            pwmG.ChangeDutyCycle(0)
            Buzz.ChangeFrequency(500 + i)
            pwmR.ChangeDutyCycle(70 - i)
            print(i - 1000)
            time.sleep(t)

except KeyboardInterrupt:
    Buzz.ChangeFrequency(0)

pwmR.stop()
pwmG.stop()
GPIO.cleanup()
