#!/usr/bin/env python
# coding=utf-8

from __future__ import division
import argparse
import Adafruit_PCA9685

pwm = Adafruit_PCA9685.PCA9685()

ap = argparse.ArgumentParser()
ap.add_argument("-c", "--channel", type=int, help="GPIO channel")
ap.add_argument("-a", "--angle", type=int, help="for enginer angle")
ap.add_argument("-o", "--on", type=int, default=0, help="for status")
ap.add_argument("-z", "--hertz", type=int, default=60, help="for GPIO driver hertz")
args = vars(ap.parse_args())

if None == args["channel"] or None == args["angle"]:
    print("please input channel and angle!")
    exit(-1)

pwm.set_pwm_freq(args["hertz"])
pwm.set_pwm(args["channel"], args["on"], args["angle"])
