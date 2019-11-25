#!/usr/bin/env python
# coding=utf-8

from __future__ import division
import argparse
import Adafruit_PCA9685

pwm = Adafruit_PCA9685.PCA9685()

ap = argparse.ArgumentParser()
ap.add_argument("-c", "-channel", type=int, help="GPIO channel")
ap.add_argument("-a", "-angle", type=int, help="for enginer angle")
args = vars(ap.parse_args())

if None == args["c"] or None == args["a"]:
    print("please input channel and angle!")
    exit(-1)

pwm.set_pwm(args["c"], 0, args["a"])
