#!/usr/bin/env python
# coding=utf-8

import cv2
import numpy as np

# 创建图片和颜色块
img = np.ones((240, 320, 3), dtype = np.uint8) * 255

# GBR 非RGB
img[100:140, 140:180] = [0,0, 255]
img[60:100, 60:100] = [0, 255, 255]
img[60:100, 220:260] = [255, 0, 0]
img[140:180, 60:100] = [255, 0, 0]
img[140:180, 220:260] = [0, 255, 255]
img[0:40, 0:40] = [226, 43, 138]
img[0:40, 280:320] = [209, 206, 0]
img[140:180, 140:180] = [255, 0, 0]

# 颜色识别
blue_lower = np.array([100,43,46])
blue_upper = np.array([124,255,255])

# 颜色转换
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# 遮罩
mask_blue = cv2.inRange(hsv, blue_lower, blue_upper)
mask = cv2.bitwise_or(mask_blue, mask_blue)
res = cv2.bitwise_and(img, img, mask = mask)

cv2.imshow('image', img)
cv2.imshow('mask', mask)
cv2.imshow('res', res)

cv2.waitKey(0)
cv2.destroyAllWindows()
