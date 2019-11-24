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
#pwm.set_pwm(0, 0, 320)
#pwm.set_pwm(1, 0, 240)
time.sleep(1)

cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier("/home/pi/Project/lib/opencv/data/haarcascades/haarcascade_frontalface_default.xml")

x = 0
thisError_x = 500
lastError_x = 100
thisError_y = 500
lastError_y = 100

Y_P = 425
X_P = 425
flag = 0
y = 0
faceBool = False

def moveSteeringEngine(x, y):
    pwm.set_pwm(14, 0, 650 - x)
    pwm.set_pwm(15, 0, 650 - y)

while True:
    ret, frame = cap.read()
    if False == ret:
        print("can't open video!")
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray)
    max_face = 0
    value_x = 0

    if 0 < len(faces):
        print("find face!")
        (x, y, w, h) = faces[0]
        cv2.rectangle(frame, (x, y), (x + h, y + h), (0, 255, 0), 2)
        result = (x, y, w, h)
        x = result[0] + w / 2
        y = result[1] + h / 2
        faceBool = True
    
    if faceBool:
        faceBool = False
        thisError_x = x - 160
        thisError_y = y - 120
        pwm_x = thisError_x * 5 + 1 * (thisError_x - lastError_x)
        pwm_y = thisError_y * 5 + 1 * (thisError_y - lastError_y)
        lastError_x = thisError_x
        lastError_y = thisError_y

        XP = pwm_x / 100
        YP = pwm_y / 100

        X_P = X_P + int(XP)
        Y_P = Y_P + int(YP)

        if 670 < X_P:
            X_P = 670
        if 0 > X_P: 
            X_P = 0
        if 650 < Y_P:
            Y_P = 650
        if 0 > Y_P:
            Y_P = 0

    tid = threading.Thread(target = moveSteeringEngine, args = (X_P, Y_P))
    tid.setDaemon(True)
    tid.start()
        
    cv2.imshow("capture", frame)
    if 119 == cv2.waitKey(1):
        break

cap.release()
cv2.destroyAllWindows()
