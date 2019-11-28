#!/usr/bin/env python
# coding=utf-8

from __future__ import division
import time
import Adafruit_PCA9685

pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(60)

time.sleep(1)

pwm.set_pwm(0, 0, 660)
time.sleep(1.5)
pwm.set_pwm(0, 0, 90)
time.sleep(1.5)
pwm.set_pwm(0, 0, 370)

time.sleep(1)
time.sleep(1)

pwm.set_pwm(1, 0, 600)
time.sleep(1.5)
pwm.set_pwm(1, 0, 200)
time.sleep(1.5)
pwm.set_pwm(1, 0, 435)

time.sleep(1)
