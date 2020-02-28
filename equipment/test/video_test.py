#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import numpy as np

bin_model = "../../models/yolo/yolov3-tiny.weights"
config = "../../models/yolo/yolov3-tiny.cfg"
label = "../../models/yolo/object_detection_classes_yolov3.txt"


def main():
    dnn = cv.dnn.readNetFromDarknet(config, bin_model)
    dnn.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
    dnn.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)
    frame = cv.imread("../data/positive/2020-17-08-26-49.jpeg")
    data = cv.dnn.blobFromImage(frame, 1.0 / 255.0, (416, 416), None, False, False)
    out_names = dnn.getUnconnectedOutLayersNames()
    dnn.setInput(data)
    outs = dnn.forward(out_names)
    t, _ = dnn.getPerfProfile()
    txt = "Inference time: %.2f ms" % (t * 1000.0 / cv.getTickFrequency())
    cv.putText(frame, txt, (0, 15), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
    h, w = frame.shape[:2]
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            if class_id != 74:
                continue
            confidence = scores[class_id]
            if 0.5 < confidence:
                center_x = int(detection[0] * w)
                center_y = int(detection[1] * h)
                width = int(detection[2] * w)
                height = int(detection[3] * h)
                left = int(center_x - width / 2)
                top = int(center_y - height / 2)
                confidences.append(float(confidence))
                boxes.append([left, top, width, height])
    cv.imshow("src", frame)
    cv.imshow("target", frame[top: top + height, left: left + width, :])
    cv.waitKey(0)
    cv.imwrite("target.jpeg", frame[top: top + height, left: left + width, :], [cv.IMWRITE_JPEG_QUALITY, 100])


if "__main__" == __name__:
    main()
    cv.destroyAllWindows()
