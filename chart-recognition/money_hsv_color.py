#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
create by afterloe<liumin@ascs.tech>
version is 1.0
"""

import cv2
import numpy as np
import imutils


# 生成颜色直方图
def color_hist(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hist_mask = cv2.calcHist([hsv], [0], None, [180], [0, 180])
    # 统计直方图识别颜色
    object_H = np.where(hist_mask == np.max(hist_mask))
    print(object_H[0])

    return object_H[0]


# 判断直方图H的值， 实现颜色识别
def color_distinguish(object_H):
    try:
        if 3 < object_H < 25:
            RMB = '20'
        elif 156 < object_H < 170:
            RMB = '100'
        elif 125 < object_H < 155:
            RMB = '5'
        elif 100 < object_H < 124:
            RMB = '10'
        elif 25 < object_H < 50:
            RMB = '1'
        elif 171 < object_H < 180:
            RMB = '50'
        else:
            RMB = 'None'
        print('RMB:', RMB, object_H)
        return RMB
    except RuntimeError as e:
        print(e)


FILE = './pic/rmb/50.png'
WINDOWS_NAME = 'img show'

img = cv2.imread(FILE, cv2.IMREAD_COLOR)
object_H = color_hist(img)
rmb = color_distinguish(object_H)

img = imutils.resize(img, 640, 320)
cv2.imshow(WINDOWS_NAME, img)
cv2.waitKey()

cv2.destroyAllWindows()
