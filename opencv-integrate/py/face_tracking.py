#!/usr/bin/env python
# coding=utf-8

from __future__ import division
import cv2
import time
import sys
import numpy as np

if 1 > len(sys.argv):
    PATH = "/home/pi/Pictures/40.jpg"
PATH = sys.argv[1]
WINDOWS_NAME = "face track"

img = cv2.imread(PATH)
face_cascade = cv2.CascadeClassifier("/home/pi/Project/lib/opencv/data/haarcascades/haarcascade_frontalface_default.xml")

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray)

max_face = 0
value_x = 0

if 0 < len(faces):
    print("face is find!")
    for (x, y, w, h) in faces:
        print("x: ", x, " y: ", y, " w: ", w, " h: ", h)
        img = cv2.rectangle(img, (x,y), (x+h, y+h), (255, 0, 0), 2)

cv2.namedWindow(WINDOWS_NAME, 0)
cv2.resizeWindow(WINDOWS_NAME, 640, 480)
cv2.imshow(WINDOWS_NAME, img)

cv2.waitKey(0)
cv2.destroyAllWindows()
