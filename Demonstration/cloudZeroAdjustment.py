#!/usr/bin/env python
# coding=utf-8

from __future__ import division
from speech_tool.speechTool import speech
import time
import Adafruit_PCA9685

pwm = Adafruit_PCA9685.PCA9685()

speech(4, "云台即将进行调零操作， 水平方向")
time.sleep(1)

pwm.set_pwm(0, 0, 660)
time.sleep(1.5)
pwm.set_pwm(0, 0, 90)
time.sleep(1.5)
pwm.set_pwm(0, 0, 370)

time.sleep(1)
speech(3, "垂直方向")
time.sleep(1)

pwm.set_pwm(1, 0, 600)
time.sleep(1.5)
pwm.set_pwm(1, 0, 200)
time.sleep(1.5)
pwm.set_pwm(1, 0, 435)

time.sleep(1)
speech(4, "摄像机云台调整完毕， 坐标 370, 435")
