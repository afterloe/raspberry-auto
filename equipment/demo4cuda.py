#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import cv2.cuda as gpu

"""

"""


def main():
    device = gpu.getDevice()
    print(device)


if "__main__" == __name__:
    main()
