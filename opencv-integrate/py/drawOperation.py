#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np

img = np.zeros((512, 512, 3), dtype= np.uint8)
cv2.line(img, (0,0), (500,500),(255,0,0),5)
cv2.circle(img, (255,255),50,(0,255,0),-1)
cv2.circle(img, (255,255),80,(255,255,0),5)
cv2.rectangle(img, (170,170),(340,340),(0,0,255),2)

cv2.putText(img, 'afterloe 你你你', (20,50),cv2.FONT_HERSHEY_COMPLEX,2,(0,255,255),2)
cv2.putText(img, 'hihihi 她她她', (80,450),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,255),2)

cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
