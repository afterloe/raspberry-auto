#!/usr/bin/env python
# coding=utf-8

import cv2
from PIL import Image
import numpy as np
import time
import sys

if 2 > len(sys.argv):
    print("please input the path of image!")
    exit(-1)

IMAGE_PATH = sys.argv[1]
WINDOWS_NAME = "window"
THUGLIF_NAME = "thuglif"

maskPath = "/home/pi/Pictures/black_Mask_176.13311148087px_1160639_easyicon.net.png"
cascpath = "/home/pi/Project/lib/opencv/data/haarcascades/haarcascade_frontalface_default.xml"

faceCascade = cv2.CascadeClassifier(cascpath)
mask = Image.open(maskPath)

def thug_mask(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray)
    background = Image.fromarray(image)

    for (x, y, w, h) in faces:
        resized_mask = maskImg.resize((w,h), Image.ANTIALIAS)
        offset = (x, y)
        background.paste(resized_mask, offset, mask = resized_mask)

    return np.asarray(background)

# img = cv2.imread(IMAGE_PATH) 

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if False == ret:
        print("read image frome vide failed!")
        break
    cv2.imshow(WINDOWS_NAME, frame)
    frame = thug_mask(frame)
    cv2.imshow(THUGLIF_NAME, frame)
    if cv2.waitKey(5)&0xFF == 27:
        break


cap.release()
cv2.destroyAllWindows()
