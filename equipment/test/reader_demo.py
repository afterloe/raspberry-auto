#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
# import pytesseract
import numpy as np


"""

"""


def main():
    image = cv.imread("./target.jpeg", cv.IMREAD_COLOR)
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    binary = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 45, 15)
    binary = cv.morphologyEx(binary, cv.MORPH_CLOSE, cv.getStructuringElement(cv.MORPH_RECT, (3, 3)))
    contours, hierarchy = cv.findContours(binary, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    dst = np.zeros(image.shape, dtype=image.dtype)
    print(len(contours))
    for index in range(len(contours)):
        contour = contours[index]
        area = cv.contourArea(contour)
        if 1000 > area or 5000 < area:
            continue
        rect = cv.minAreaRect(contours[index])
        box = cv.boxPoints(rect)  # opencv 中的api， 快速绘制带有角度的矩形
        box = np.int32(box)  # 将结果转换为int32 类型
        print(box)  # 左、下、右、上
        cv.drawContours(image, [box], 0, (0, 0, 255), 2, cv.LINE_8)

    # text = pytesseract.image_to_string(image)
    # print(text)
    cv.imshow("input", image)
    cv.imshow("binary", binary)
    # cv.imshow("dst", dst)
    cv.waitKey(0)


if "__main__" == __name__:
    main()
    cv.destroyAllWindows()
