#!/usr/bin/env python
# coding=utf-8

from __future__ import division
import Adafruit_PCA9685
import sys

pwm = Adafruit_PCA9685.PCA9685()

input_angle = int(sys.argv[1])
angle = 4096 * ((input_angle * 11) + 500) / 20000
pwm.set_pwm(15, 0, int(angle))
