#!/usr/bin/env python
# coding=utf-8

from __future__ import division
import cv2
import time
import numpy as np

cap = cv2.VideoCapture(0)

yellow_hsv_min = np.array([26, 43, 46])
yellow_hsv_max = np.array([34, 255, 255])

while True:
    ret, frame = cap.read()

    frame = cv2.GaussianBlur(frame, (5,5), 0) # 高斯模糊
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, yellow_hsv_min, yellow_hsv_max)

    mask = cv2.erode(mask, None, iterations = 2)
    mask = cv2.dilate(mask, None, iterations = 2)
    mask = cv2.GaussianBlur(mask, (3,3), 0)
    res = cv2.bitwise_and(frame, frame, mask = mask)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, 
                           cv2.CHAIN_APPROX_SIMPLE)[-2]

    if len(cnts) > 0:
        cnt = max(cnts, key = cv2.contourArea)
        (x,y), radius = cv2.minEnclosingCircle(cnt)
        cv2.circle(frame, (int(x), int(y)), int(radius) * 2,
                  (255, 0, 255), 2)
        print('x: ', x, " y: ", y)

    cv2.imshow('cat Capture', frame)
    if 119 == cv2.waitKey(1):
        break

cap.release()
cv2.destroyAllWindows()
