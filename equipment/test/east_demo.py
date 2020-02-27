#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import time
import numpy as np

"""

"""

model_bin = "../../models/east_net/frozen_east_text_detection.pb"
layer_names = ["feature_fusion/Conv_7/Sigmoid", "feature_fusion/concat_3"]


def main():
    dnn = cv.dnn.readNet(model_bin)
    dnn.setPreferableBackend(cv.dnn.DNN_BACKEND_CUDA)
    dnn.setPreferableTarget(cv.dnn.DNN_TARGET_CUDA)
    image = cv.imread("./target.jpeg")
    cv.imshow("src", image)
    (H, W) = image.shape[:2]
    rH = H / float(320)
    rW = W / float(320)
    data = cv.dnn.blobFromImage(image, 1.0, (320, 320), (123.68, 116.78, 103.94), True, False)
    start = time.time()
    dnn.setInput(data)
    scores, geometry = dnn.forward(layer_names)
    end = time.time()
    print("[INFO] test detection took {:.6f} seconds".format(end - start))
    num_rows, num_cols = scores.shape[2: 4]
    rects = []
    confidences = []
    for y in range(0, num_rows):
        scores_data = scores[0, 0, y]
        x_data_0 = geometry[0, 0, y]
        x_data_1 = geometry[0, 1, y]
        x_data_2 = geometry[0, 2, y]
        x_data_3 = geometry[0, 3, y]
        angles_data = geometry[0, 4, y]
        for x in range(0, num_cols):
            if scores_data[x] < 0.5:
                continue
            off_set_x, off_set_y = x * 4.0, y * 4.0
            angle = angles_data[x]
            cos = np.cos(angle)
            sin = np.cos(angle)
            h = x_data_0[x] + x_data_2[x]
            w = x_data_1[x] + x_data_3[x]
            end_x = int(off_set_x + (cos * x_data_1[x]) + (sin * x_data_2[x]))
            end_y = int(off_set_y - (sin * x_data_1[x]) + (cos * x_data_2[x]))
            start_x = int(end_x - w)
            start_y = int(end_y - h)
            rects.append([start_x, start_y, end_x, end_y])
            confidences.append(float(scores_data[x]))

    boxes = cv.dnn.NMSBoxes(rects, confidences, 0.5, 0.8)

    for i in boxes:
        i = i[0]
        start_x, start_y, end_x, end_y = rects[i]
        start_x = int(start_x * rW)
        start_y = int(start_y * rH)
        end_x = int(end_x * rW)
        end_y = int(end_y * rH)
        cv.rectangle(image, (start_x, start_y), (end_x, end_y), (255, 0, 0), 2)
    cv.imshow("result", image)
    cv.waitKey(0)


if "__main__" == __name__:
    main()
    cv.destroyAllWindows()
