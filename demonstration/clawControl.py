#!/usr/bin/env python
# coding=utf-8

from __future__ import division
import time
import Adafruit_PCA9685

pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(60)

i = 0
while i < 5:
    i += 1
    pwm.set_pwm(11, 0, 370)
    time.sleep(1)
    pwm.set_pwm(11, 0, 480)
    time.sleep(1)
    pwm.set_pwm(11, 0, 400)
