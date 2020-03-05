#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import time
import numpy as np

"""

"""

bin_model = "../models/yolo/yolov3-tiny.weights"
config = "../models/yolo/yolov3-tiny.cfg"
label = "../models/yolo/object_detection_classes_yolov3.txt"


def main():
    capture = cv.VideoCapture(0)
    labels = None
    with open(label, "r") as f:
        labels = f.read().rstrip("\n").split("\n")
    print(labels)
    dnn = cv.dnn.readNetFromDarknet(config, bin_model)
    dnn.setPreferableBackend(cv.dnn.DNN_BACKEND_CUDA)
    dnn.setPreferableTarget(cv.dnn.DNN_TARGET_CUDA)

    # cv.namedWindow("living", cv.WINDOW_AUTOSIZE)
    # cv.resizeWindow("living", 600, 300)
    # cv.resizeWindow("yolov3 demo", 600, 300)

    while True:
        ret, frame = capture.read()
        if False is ret:
            print("video is ended.")
            break
        h, w = frame.shape[:2]
        data = cv.dnn.blobFromImage(frame, 1.0 / 255.0, (416, 416), None, False, False)
        out_names = dnn.getUnconnectedOutLayersNames()
        dnn.setInput(data)
        outs = dnn.forward(out_names)
        class_ids = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if 67 != class_id:
                    continue
                if 0.5 < confidence:
                    center_x = int(detection[0] * w)
                    center_y = int(detection[1] * h)
                    width = int(detection[2] * w)
                    height = int(detection[3] * h)
                    left = int(center_x - width / 2)
                    top = int(center_y - height / 2)
                    class_ids.append(int(class_id))
                    confidences.append(float(confidence))
                    boxes.append([left, top, width, height])
        indices = cv.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        for i in indices:
            i = i[0]
            box = boxes[i]
            left, top, width, height = box[:4]
            cv.rectangle(frame, (left, top), (left + width, top + height), (0, 0, 255), 2, cv.LINE_AA)
            cv.putText(frame, "target", (left, top), cv.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 0), 2)
            print(class_ids[i])

        cv.imshow("yolov3 demo", frame)
        key = cv.waitKey(100)
        if 27 == key:
            print("enter esc")
            break
        if 119 == key:
            print("enter w to save image.")
            cv.imwrite("%s.jpeg" % (time.strftime("%Y-%d-%H-%M-%S", time.gmtime(time.time()))), frame[top: top + height, left: left + width, :],
                       [cv.IMWRITE_JPEG_QUALITY, 100])
    capture.release()


if "__main__" == __name__:
    main()
    cv.destroyAllWindows()
