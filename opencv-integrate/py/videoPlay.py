#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
create by afterloe<liumin@ascs.tech>
version is 1.4
"""

import cv2

cap = cv2.VideoCapture(0)
while cap.isOpened():
    ret, frame = cap.read()
    if ret:
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()
