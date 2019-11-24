#!/usr/bin/env python
# coding=utf-8

from __future__ import division
import Adafruit_PCA9685
import sys

pwm = Adafruit_PCA9685.PCA9685()

if 2 > len(sys.argv):
    print("input x, y!")
    exit(-1)

pwm.set_pwm_freq(60)
pwm.set_pwm(14, 0, int(sys.argv[1]))
