#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
from imutils.object_detection import non_max_suppression
import numpy as np
import time

"""

"""

model_bin = "../../models/east_net/frozen_east_text_detection.pb"
layer_names = ["feature_fusion/Conv_7/Sigmoid", "feature_fusion/concat_3"]
padding = 5


def main():
    dnn = cv.dnn.readNet(model_bin)
    dnn.setPreferableBackend(cv.dnn.DNN_BACKEND_CUDA)
    dnn.setPreferableTarget(cv.dnn.DNN_TARGET_CUDA)
    image = cv.imread("G:\\Project\\opencv-ascs-resources\\meter_pointer_roi\\2020-03-05_22-18-30.jpeg")
    # image = cv.imread("./target.jpeg")
    cv.imshow("src", image)
    (h, w) = image.shape[:2]
    r_h = h / float(320)
    r_w = w / float(320)
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
            sin = np.sin(angle)
            h = x_data_0[x] + x_data_2[x]
            w = x_data_1[x] + x_data_3[x]
            end_x = int(off_set_x + (cos * x_data_1[x]) + (sin * x_data_2[x]))
            end_y = int(off_set_y - (sin * x_data_1[x]) + (cos * x_data_2[x]))
            start_x = int(end_x - w)
            start_y = int(end_y - h)
            rects.append([start_x, start_y, end_x, end_y])
            confidences.append(float(scores_data[x]))
    # 最大区域抑制
    boxes = non_max_suppression(np.array(rects), probs=confidences)
    # boxes = cv.dnn.NMSBoxes(rects, confidences, 0.5, 0.8)  # 抑制目标， 最大目标
    result = np.zeros(image.shape[:2], dtype=image.dtype)
    # for i in boxes:
    #     i = i[0]
    #     start_x, start_y, end_x, end_y = rects[i]
    #     start_x = int(start_x * r_w)
    #     start_y = int(start_y * r_h)
    #     end_x = int(end_x * r_w)
    #     end_y = int(end_y * r_h)
    #     cv.rectangle(result, (start_x, start_y), (end_x, end_y), (255, 0, 0), 2)
    for start_x, start_y, end_x, end_y in boxes:
        start_x = int(start_x * r_w)
        start_y = int(start_y * r_h)
        end_x = int(end_x * r_w)
        end_y = int(end_y * r_h)
        cv.rectangle(image, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)

    kernel = cv.getStructuringElement(cv.MORPH_RECT, (5, 1))
    result = cv.morphologyEx(result, cv.MORPH_DILATE, kernel)
    contours, hierachy = cv.findContours(result, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    text_boxes = []
    for index in range(len(contours)):
        box = cv.boundingRect(contours[index])
        if box[2] < 10 or box[3] < 10:
            continue
        # cv.rectangle(image, (box[0], box[1]), (box[0] + box[2], box[1] + box[3]), (255, 0, 0), 2, cv.LINE_AA)
        # x, y, w, h
        text_boxes.append((box[0], box[1], box[0] + box[2], box[1] + box[3]))

    nums = len(text_boxes)
    for i in range(nums):
        for j in range(i + 1, nums, 1):
            y_i = text_boxes[i][1]
            y_j = text_boxes[j][1]
            if y_i > y_j:
                temp = text_boxes[i]
                text_boxes[i] = text_boxes[j]
                text_boxes[j] = temp
    for x, y, w, h in text_boxes:
        # name = "./{}.jpeg".format(
        #     time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime(time.time())))
        # print("{} save in {}".format("INFO", name))
        roi = image[y: h + padding, x: w, :]
        # cv.imwrite(name, roi)
        text_area_detect(roi)

    cv.imshow("finder", image)
    # cv.imshow("result", result)
    cv.waitKey(0)


def text_area_detect(roi):
    gray = cv.cvtColor(roi, cv.COLOR_BGR2GRAY)
    binary = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 45, 15)
    cv.imshow("text_roi", gray)
    cv.waitKey(0)


if "__main__" == __name__:
    main()
    cv.destroyAllWindows()
