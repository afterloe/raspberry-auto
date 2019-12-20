#!/usr/bin/env python
# coding=utf-8

from __future__ import division
import time
import Adafruit_PCA9685

pwm = Adafruit_PCA9685.PCA9685()

servo_min = 150
servo_max = 600

def set_servo_pulse(channel, pulse):
    pulse_length = 100 * 10000
    pulse_length //= 60
    print('{0} us per period.'.format(pulse_length))
    pulse_length //= 4096
    print('{0} us per bit'.format(pulse_length))

    pulse *= 10
    pulse //= pulse_length
    pwm.setpwm(channel, 0, pulse)

def set_servo_angle(channel, angle):
    angle = 4096 * ((angle * 11) + 500) / 20000
    pwm.set_pwm(channel, 0, int(angle))

pwm.set_pwm_freq(50)

set_servo_angle(1, 100)
set_servo_angle(0, 30)
time.sleep(0.8)

print("moving servo on channel 0, press ctrl-c to quit...")
