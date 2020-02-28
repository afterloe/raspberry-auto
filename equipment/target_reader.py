#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import pytesseract

"""

"""


def main():
    # pytesseract.pytesseract.tesseract_cmd = "D:/Program Files/Tesseract-OCR/tesseract.exe"
    image = cv.imread("C:/Users/afterloe/Desktop/A8574D96-DDD0-40e6-B324-B9828AECE678.png")
    text = pytesseract.image_to_string(image)
    print(text)
    # pass


if "__main__" == __name__:
    main()
