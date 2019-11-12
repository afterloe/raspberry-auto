#!/usr/bin/env python
# coding=utf-8

import RPi.GPIO as R
import time

Buzzer = 17
R.setwarnings(False)

R.setmode(R.BCM)
R.setup(Buzzer, R.OUT)

buzz = R.PWM(Buzzer, 440)
buzz.start(50)

for i in range(0, 5):
    for i in range(0, 550):
        buzz.ChangeFrequency(i + 1)
        time.sleep(0.01)
    for i in range(550, 0, -1):
        buzz.ChangeFrequency(i)
        time.sleep(0.01)

buzz.stop()
R.cleanup()
