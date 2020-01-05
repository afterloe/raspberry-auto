#!/usr/bin/env python
# coding=utf-8

import cv2
import sys
import numpy as np

if 1 > len(sys.argv):
    print("missing arg, like path of image! \r\n")
    exit(-1)

img = cv2.imread(sys.argv[1])

black_lower = np.array([0, 0, 0])
black_upper = np.array([180, 255, 46])

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

mask_black = cv2.inRange(hsv, black_lower, black_upper)
mask = cv2.bitwise_or(mask_black, mask_black)
res = cv2.bitwise_and(img, img, mask = mask)

cv2.namedWindow("img", 0)
cv2.resizeWindow("img", 640, 480)
cv2.imshow("img", img)

cv2.namedWindow("mask", 0)
cv2.resizeWindow("mask", 640, 480)
cv2.imshow("mask", mask)

cv2.namedWindow("res", 0)
cv2.resizeWindow("res", 640, 480)
cv2.imshow("res", res)

cv2.waitKey(0)
cv2.destroyAllWindows()
