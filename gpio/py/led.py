#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
* create by afterloe
* MIT License
* version is 1.0
"""

import RPi.GPIO as GPIO

import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)

for i in range(0, 15):
    GPIO.output(5, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(5, GPIO.LOW)
    GPIO.output(6, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(6, GPIO.LOW)

GPIO.cleanup()
