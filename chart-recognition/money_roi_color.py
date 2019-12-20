#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
create by afterloe<liumin@ascs.tech>
version is 1.0
"""

import cv2
import numpy as np
import imutils


def find_ROI(img):
    blur = cv2.GaussianBlur(img, (5, 5), 0)
    gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
    ret, th = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    mask = cv2.erode(th, None, iterations=4)
    mask = cv2.dilate(mask, None, iterations=4)
    cv2.bitwise_not(mask, mask)
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if 0 < len(contours):
        cnt = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(cnt)
        img = cv2.rectangle(img, (x, y), (x + w, y + w), (0, 255, 0), 3)
        img_ROI = img[y:y + h, x:x + w]
    else:
        img_ROI = img
    return img_ROI


def color_hist(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hist_mask = cv2.calcHist([hsv], [0], None, [180], [0, 180])
    object_h = np.where(hist_mask == np.max(hist_mask))
    print(object_h[0])
    return object_h[0]


def color_distinguish(object_h):
    try:
        if 3 < object_h < 25:
            RMB = '20'
        elif 156 < object_h < 170:
            RMB = '100'
        elif 125 < object_h < 155:
            RMB = '5'
        elif 100 < object_h < 124:
            RMB = '10'
        elif 25 < object_h < 50:
            RMB = '1'
        elif 171 < object_h < 180:
            RMB = '50'
        else:
            RMB = 'None'
        print('RMB:', RMB, object_h)
        return RMB
    except RuntimeError as err:
        print(err)


img = cv2.imread("./pic/1yuan.jpg")
img_roi = find_ROI(img)
object_h = color_hist(img_roi)
rmb = color_distinguish(object_h)
text = rmb + "元人民币，hsv特征为" + str(object_h[0])
print(text)
img = imutils.resize(img, 640)
cv2.imshow("image", img)
cv2.waitKey()
cv2.destroyAllWindows()
