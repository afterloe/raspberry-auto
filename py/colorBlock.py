#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
* create by afterloe
* MIT License
* version 1.0
"""

import cv2
import numpy as np

# 创建图片和颜色块
img = np.ones((240, 320, 3), dtype=np.uint8) * 255
img[100:140, 140:180] = [0,0,255]
img[60:100, 60:100] = [0,255,255]
img[60:100, 220:260] = [255,0,0]
img[140:180, 60:100] = [255,0,0]
img[140:180, 220:260] = [0,255,255]

# 黄红两色的hsv阈值
yello_lower=np.array([26,43,46])
yello_upper=np.array([34,255,255])
red_lower=np.array([0,43,46])
red_upper=np.array([10,255,255])

# 颜色转换
hsv=cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# 遮罩
mask_yellow=cv2.inRange(hsv, yello_lower, yello_upper)
mask_red=cv2.inRange(hsv, red_lower, red_upper)
mask=cv2.bitwise_or(mask_yellow, mask_red)
res=cv2.bitwise_and(img, img, mask=mask)

cv2.imshow('imgage', img)
cv2.imshow('mask', mask)
cv2.imshow('res', res)

cv2.waitKey(0)
cv2.destroyAllWindows()
