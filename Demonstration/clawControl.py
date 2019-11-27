#!/usr/bin/env python
# coding=utf-8

from __future__ import division
import time
import Adafruit_PCA9685

pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(60)

pwm.set_pwm(2, 0, 340)
time.sleep(2)
pwm.set_pwm(2, 0, 490)
time.sleep(2)
pwm.set_pwm(2, 0, 340)
