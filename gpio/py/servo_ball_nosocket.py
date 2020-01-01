#!/usr/bin/env python
# coding=utf-8

from __future__ import division
import cv2
import Adafruit_PCA9685

import time
import numpy as np
import threading

pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(60)
pwm.set_pwm(14, 0, 580)
pwm.set_pwm(15, 0, 580)
time.sleep(1)

cap = cv2.VideoCapture(0)
hsv_min = np.array([45,43,46])
hsv_max = np.array([77,255,255])

x = 0
thisError_x = 500
lastError_x = 100
thisError_y = 500
lastError_y = 100

Y_P = 425
X_P = 425
flag = 0
y = 0

def xx(X_P, Y_P):
    pwm.set_pwm(14, 0, 650 - X_P)
    pwm.set_pwm(15, 0, 650 - Y_P)

while 1:
    ret, frame = cap.read()
    if False == ret:
        print("read image from video failed!")
        break;
    frame = cv2.GaussianBlur(frame, (5, 5), 0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, hsv_min, hsv_max)
    mask = cv2.erode(mask, None, iterations = 2)
    mask = cv2.dilate(mask, None, iterations = 2)
    mask = cv2.GaussianBlur(mask, (3, 3), 0)
    res = cv2.bitwise_and(frame ,frame, mask = mask)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

    if 0 < len(cnts):
        print("target find!")
        cnt = max(cnts, key = cv2.contourArea)
        (x, y), radius = cv2.minEnclosingCircle(cnt)
        cv2.circle(frame, (int(x), int(y)), int(radius), (255, 0, 255), 2)
        thisError_x = x - 160
        thisError_y = y - 120
        pwm_x = thisError_x * 3 + 1 * (thisError_x - lastError_x)
        pwm_y = thisError_y * 3 + 1 * (thisError_y - lastError_y)
        lastError_x = thisError_x
        lastError_y = thisError_y
        XP = pwm_x / 100
        YP = pwm_y / 100
        X_P = X_P + int(XP)
        Y_P = Y_P + int(YP)

        if 670 < X_P:
            X_P = 650
        if 0 > X_P:
            X_P = 0
        if 650 < Y_P:
            Y_P = 650
        if 0 > Y_P:
            Y_P = 0
        print('x', x, X_P)
    
    tid = threading.Thread(target = xx, args = (X_P, Y_P,))
    tid.setDaemon(True)
    tid.start()

#    cv2.imshow("live...", frame)
    if 119 == cv2.waitKey(5):
        break

cap.release()
cv2.destroyAllWindows()
