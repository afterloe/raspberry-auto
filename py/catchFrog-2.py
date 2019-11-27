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

cap = cv2.VideoCapture(0)
hsv_min = np.array([45,43,46])
hsv_max = np.array([77,255,255])

def xx(X_P, Y_P):
    if 660 < X_P:
        X_P = 660
    if 90 > X_P:
        X_P = 90
    if 600 < Y_P:
        Y_P = 600
    if 190 > Y_P:
        Y_P = 190
    pwm.set_pwm(0, 0, X_P)
    pwm.set_pwm(1, 0, Y_P)

videoWidth = cap.get(cv2.CAP_PROP_FRAME_WIDTH) # 640
videoHeight = cap.get(cv2.CAP_PROP_FRAME_HEIGHT) # 480
x_p = 370
y_p = 435
flag = 1

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
        cnt = max(cnts, key = cv2.contourArea)
        (x, y), radius = cv2.minEnclosingCircle(cnt)
        x = int(x)
        y = int(y)
        radius = int(radius)
        cv2.rectangle(frame, (x - radius, y - radius), (x + radius, y + radius), (0, 255, 0), 2)

        if x - radius > videoWidth / 2:
            print("右")
            x_p -= flag
        else:
            print("左")
            x_p += flag

        if y - radius > videoHeight / 2:
            print("下")
            y_p -= flag
        else:
            print("上")
            y_p += flag

        print("x:%d, y:%d" % (x_p, y_p))
        tid = threading.Thread(target = xx, args = (x_p, y_p))
        tid.setDaemon(True)
        tid.start()

    cv2.imshow("cat rog", frame)
    if 119 == cv2.waitKey(1):
        break

cap.release()
cv2.destroyAllWindows()
