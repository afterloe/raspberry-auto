#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2 as cv
import numpy as np
import os

"""

"""

positive_dir = "../data/positive/"
negative_dir = "../data/negative/"


def get_hog_descriptor(image):
    hog = cv.HOGDescriptor()
    h, w = image.shape[:2]
    rate = 64 / w
    image = cv.resize(image, (64, np.int(rate * h)))
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    bg = np.zeros((128, 64), dtype=np.uint8)
    bg[:, :] = 127
    h, w = gray.shape
    dy = (128 - h) // 2
    bg[dy: h + dy, :] = gray
    fv = hog.compute(bg, winStride=(8, 8), padding=(0, 0))
    return fv


def generator_data_set():
    train_data = []
    labels = []
    for file_name in os.listdir(positive_dir):
        img_dir = os.path.join(positive_dir, file_name)
        img = cv.imread(img_dir)
        hog_desc = get_hog_descriptor(img)
        one_fv = np.zeros([len(hog_desc)], dtype=np.float32)
        for i in range(len(hog_desc)):
            one_fv[i] = hog_desc[i][0]
        train_data.append(one_fv)
        labels.append(1)
    for file_name in os.listdir(negative_dir):
        img_dir = os.path.join(negative_dir, file_name)
        img = cv.imread(img_dir)
        hog_desc = get_hog_descriptor(img)
        one_fv = np.zeros([len(hog_desc)], dtype=np.float32)
        for i in range(len(hog_desc)):
            one_fv[i] = hog_desc[i][0]
        train_data.append(one_fv)
        labels.append(-1)
    return np.array(train_data, dtype=np.float32), np.array(labels, dtype=np.int32)


def main():
    svm = cv.ml.SVM_create()
    svm.setKernel(cv.ml.SVM_LINEAR)
    svm.setType(cv.ml.SVM_C_SVC)
    svm.setC(2.67)
    svm.setGamma(5.383)
    train_data, response = generator_data_set()
    response = np.reshape(response, [-1, 1])
    svm.train(train_data, cv.ml.ROW_SAMPLE, response)
    svm.save("svm_data.dat")


if "__main__" == __name__:
    main()
