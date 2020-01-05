#!/usr/bin/env python
# coding=utf-8

from __future__ import division
import time
import Adafruit_PCA9685

pwm = Adafruit_PCA9685.PCA9685()

for num in range(90, 890):
    pwm.set_pwm(14, 0, num)
    time.sleep(1)

#pwm.set_pwm(14, 0, int(angle))
