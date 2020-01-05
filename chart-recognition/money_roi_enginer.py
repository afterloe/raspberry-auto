#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
create by afterloe<liumin@ascs.tech>
version is 1.0
"""

import cv2
import time
import numpy as np

DELAY = 0.02
USE_CAM = 1
IS_FOUND = 0
MORPH = 7
CANNY = 250
_width = 600.0
_height = 420.0
_margin = 0.0

if USE_CAM:
    video_capture = cv2.VideoCapture(0)


def color_hist(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hist_mask = cv2.calcHist([hsv], [0], None, [180], [0, 180])
    object_H = np.where(hist_mask == np.max(hist_mask))
    print(object_H[0])
    return object_H[0]


corners = np.array(
    [
        [[_margin, _margin]],
        [[_margin, _height + _margin]],
        [[_width + _margin, _height + _margin]],
        [[_width + _margin, _margin]],
    ]
)
pts_dst = np.array(corners, np.float32)

sendTime = 0
while True:

    if USE_CAM:
        ret, rgb = video_capture.read()
    else:
        ret = 1
        rgb = cv2.imread("opencv.jpg", 1)
    if ret:
        gray = cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY)
        gray = cv2.bilateralFilter(gray, 1, 10, 120)
        edges = cv2.Canny(gray, 10, CANNY)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (MORPH, MORPH))
        closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
        contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for cont in contours:
            if cv2.contourArea(cont) > 5000:
                arc_len = cv2.arcLength(cont, True)
                approx = cv2.approxPolyDP(cont, 0.1 * arc_len, True)
                if len(approx) == 4:
                    IS_FOUND = 1
                    pts_src = np.array(approx, np.float32)
                    h, status = cv2.findHomography(pts_src, pts_dst)
                    out = cv2.warpPerspective(rgb, h, (int(_width + _margin * 2), int(_height + _margin * 2)))
                    cv2.drawContours(rgb, [approx], -1, (255, 0, 0), 2)
                else:
                    pass

        cv2.namedWindow('edges', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('edges', edges)
        cv2.namedWindow('rgb', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('rgb', rgb)
        if IS_FOUND:
            cv2.namedWindow('out', cv2.WINDOW_AUTOSIZE)
            cv2.imshow('out', out)
            cv2.imwrite('out.png', out)
            img = cv2.imread('out.png', 1)
            object_H = color_hist(img)
            try:
                currentTime = time.time()
                if 11 < object_H < 25:
                    RMB = 20
                elif 35 < object_H < 43:
                    RMB = 1
                elif 50 < object_H < 80:
                    RMB = 50
                elif 100 < object_H < 124:
                    RMB = 10
                elif 125 < object_H < 155:
                    RMB = 5
                elif 156 < object_H < 180:
                    RMB = 100

                else:
                    RMB = 'none'
                print('RMB:', RMB, 'yuan')

            except RuntimeError as err:
                print(err)
                pass
            cv2.imshow('image', img)
        if cv2.waitKey(27) & 0xFF == ord('q'):
            break
        time.sleep(DELAY)
    else:
        print("Stopped")
        break
if USE_CAM:
    video_capture.release()
cv2.destroyAllWindows()
