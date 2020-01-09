#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
create by afterloe<liumin@ascs.tech>
version is 1.4
"""

import cv2 as cv


cap = cv.VideoCapture(0)
cv.namedWindow("frame", cv.WINDOW_AUTOSIZE)
while cap.isOpened():
    ret, frame = cap.read()
    if ret:
        cv.imshow('frame',frame)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
cv.destroyAllWindows()
