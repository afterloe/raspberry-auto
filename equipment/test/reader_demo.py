#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import pytesseract
import numpy as np


"""

"""


def main():
    image = cv.imread("./target.jpeg", cv.IMREAD_COLOR)
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray, (3, 3), 0)
    _, binary = cv.threshold(blur, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (1, 1))
    binary = cv.morphologyEx(binary, cv.MORPH_OPEN, kernel)
    lines_p = cv.HoughLinesP(binary, 1, np.pi / 180, 5, None, 50, 10)
    if None is lines_p:
        print("can't find line")
        return
    for index in range(len(lines_p)):
        line = lines_p[index][0]  # 检测到的直线信息
        cv.line(image, (line[0], line[1]), (line[2], line[3]), (255, 0, 0), 1, cv.LINE_AA)

    # text = pytesseract.image_to_string(image)
    # print(text)
    cv.imshow("input", image)
    cv.imshow("binary", binary)
    cv.waitKey(0)


if "__main__" == __name__:
    main()
    cv.destroyAllWindows()
