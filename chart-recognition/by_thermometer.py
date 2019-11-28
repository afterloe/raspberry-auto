#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
create by afterloe<liumin@ascs.tech>
version is 1.0
"""

import cv2

FILE = './pic/1.jpg'
WINDOWS_NAME = 'img show'

img = cv2.imread(FILE, cv2.IMREAD_COLOR)

cv2.imshow(WINDOWS_NAME, img)
cv2.waitKey()

cv2.destroyAllWindows()
