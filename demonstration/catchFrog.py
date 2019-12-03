#!/usr/bin/env python
# coding=utf-8

from __future__ import division
import cv2
import Adafruit_PCA9685

import time
import numpy as np
import threading
import math

pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(60)

cap = cv2.VideoCapture(0)
hsv_min = np.array([45,83,86])
hsv_max = np.array([77,255,255])
zero_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH) / 2  # 640 / 2 
zero_hight = cap.get(cv2.CAP_PROP_FRAME_HEIGHT) / 2  # 480 / 2



class Point(object):
    def __init__(self, x, y, step):
        self.__x = x
        self.__y = y
        self.__step = step

    def xAdd(self, step=None):
        if None is not step:
            self.__x += step
        else:
            self.__x += self.__step
    
    def yAdd(self, step=None):
        if None is not step:
            self.__y += step
        else:
            self.__y += self.__step

    def xSub(self, step=None):
        if None is not step:
            self.__x -= step
        else:
            self.__x -= self.__step

    def ySub(self, step=None):
        if None is not step:
            self.__y -= step
        else:
            self.__y -= self.__step

    def getAddr(self):
        return self.__x, self.__y


def calculationLogic(x, y):
    a = math.pow((x - zero_width), 2)
    b = math.pow((y - zero_hight), 2)
    return math.sqrt(a + b)


def driveReverse():
    pwm.set_pwm(12, 0, 550)
    pwm.set_pwm(14, 0, 550)


def driveBraking():
    pwm.set_pwm(12, 0, 350)
    pwm.set_pwm(14, 0, 350)


def driveAhead():
    pwm.set_pwm(12, 0, 150)
    pwm.set_pwm(14, 0, 150)


def driveLeft():
    pwm.set_pwm(12, 0, 350)
    pwm.set_pwm(14, 0, 150)


def driveRight():
    pwm.set_pwm(12, 0, 150)
    pwm.set_pwm(14, 0, 350)


def moveSteering(X_P, Y_P):
    if 600 < X_P:
        X_P = 600
    if 100 > X_P:
        X_P = 100
    if 590 < Y_P:
        Y_P = 590
    if 200 > Y_P:
        Y_P = 200
    pwm.set_pwm(0, 0, X_P)
    pwm.set_pwm(1, 0, Y_P)


def findTarget(frame):
    frame = cv2.GaussianBlur(frame, (5, 5), 0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, hsv_min, hsv_max)
    mask = cv2.erode(mask, None, iterations = 2)
    mask = cv2.dilate(mask, None, iterations = 2)
    mask = cv2.GaussianBlur(mask, (3, 3), 0)
    res = cv2.bitwise_and(frame ,frame, mask = mask)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    if 0 >= len(cnts):
        return False, cnts
    else:
        return True, cnts


def targetTracking(cnts, p, frame=None):
    cnt = max(cnts, key=cv2.contourArea)
    (x, y), radius = cv2.minEnclosingCircle(cnt)
    if 10 > radius:
        return 
    x, y, radius = int(x), int(y), int(radius)
    if None is not frame:
        cv2.rectangle(frame, (x - radius, y - radius), (x + radius, y + radius),
                      (0, 255, 0), 2)
    if calculationLogic(x, y) < 50:
        return
    if x > zero_width:
        print("右")
        p.xSub()
    else:
        print("左")
        p.xAdd()

    if y > zero_hight:
        print("下")
        p.ySub()
    else:
        print("上")
        p.yAdd()
    print("move to %d, %d" % (p.getAddr()))
    tid = threading.Thread(target = moveSteering, args = (p.getAddr()))
    tid.setDaemon(True)
    tid.start()

p = Point(250, 390, 1)
x, y = p.getAddr()
moveSteering(x, y)

while True:
    ret, frame = cap.read()
    if False == ret:
        print("read image from video failed!")
        break;
    find, cnts = findTarget(frame)
    if find:
        targetTracking(cnts, p, frame)
    cv2.imshow("cat rog", frame)
    if 119 == cv2.waitKey(5):  # pass w
        break

cap.release()
cv2.destroyAllWindows()
