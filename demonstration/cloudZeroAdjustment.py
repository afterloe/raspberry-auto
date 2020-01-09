#!/usr/bin/env python
# coding=utf-8

from __future__ import division
from speech_tool.speechTool import speech
import time
import Adafruit_PCA9685


speech(4, "自动化装备即将进行调零操作，共四个关节")
time.sleep(1)

SLEEP_TIME = 1.5

pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(60)

time.sleep(1)

pwm.set_pwm(0, 0, 600)
time.sleep(SLEEP_TIME)
pwm.set_pwm(0, 0, 100)
time.sleep(SLEEP_TIME)
pwm.set_pwm(0, 0, 251)

time.sleep(1)

pwm.set_pwm(1, 0, 200)
time.sleep(SLEEP_TIME)
pwm.set_pwm(1, 0, 590)
time.sleep(SLEEP_TIME)
pwm.set_pwm(1, 0, 395)

time.sleep(1)

pwm.set_pwm(2, 0, 250)
time.sleep(SLEEP_TIME)
pwm.set_pwm(2, 0, 590)
time.sleep(SLEEP_TIME)
pwm.set_pwm(2, 0, 470)

time.sleep(1)
pwm.set_pwm(3, 0, 620)
time.sleep(SLEEP_TIME)
pwm.set_pwm(3, 0, 470)
time.sleep(SLEEP_TIME)
pwm.set_pwm(3, 0, 540)

speech(3, "自动化装备调零完毕")
