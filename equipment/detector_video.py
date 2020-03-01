#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import imutils
from imutils.object_detection import non_max_suppression
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import time


def main():
    print("[INFO] starting video stream...")
    vs = VideoStream(src=0).start()
    time.sleep(1.0)
    fps = FPS().start()
    dnn = cv.dnn.readNet("model of path")
    layer_names = []
    while True:
        frame = vs.read()
        if None is frame:
            break
        # 调整帧大小，保持纵横比
        frame = imutils.resize(frame, width=1000)
        h, w = frame.shape[:2]
        # float 加快计算速度
        r_w = w / float(320)
        r_h = h / float(320)
        # 调整帧的大小，忽略纵横比
        frame = cv.resize(frame, (320, 320))
        blob = cv.dnn.blobFromImage(frame, 1.0, (320, 320), (123.68, 116.78, 103.94), True, False)
        dnn.setInput(blob)
        scores, geometry = dnn.forward(layer_names)
        rects, confidences = decode_predictions(scores, geometry)
        boxes = non_max_suppression(np.array(rects), probs=confidences)
        for x, y, w, h in boxes:
            x = int(x * r_w)
            y = int(y * r_h)
            w = int(w * r_w)
            h = int(h * r_h)
            cv.rectangle(frame, (x, y), (w, h), (0, 255, 0), 2)
        fps.update()
        cv.imshow("text detection", frame)
        key = cv.waitKey(1) & 0xff
        if ord("q") == key:
            print("[INFO] enter q to close this...")
            break
        fps.stop()
        print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
        print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
    vs.stop()


if "__main__" == __name__:
    main()
    cv.destroyAllWindows()
