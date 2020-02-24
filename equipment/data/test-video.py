#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import time


capture = cv.VideoCapture(0)
sequence = 0

while True:
    ret, frame = capture.read()
    if False is ret:
        print("video is ended.")
        break
    cv.imshow("living", frame)
    key = cv.waitKey(10)
    if 27 == key:
        print("enter esc")
        break
    if 119 == key:
        print("enter w to save image.")
        cv.imwrite("%s.jpeg" % (time.strftime("%Y-%d-%H-%M-%S", time.gmtime(time.time()))), frame, [cv.IMWRITE_JPEG_QUALITY, 100])

capture.release()
cv.destroyAllWindows()
