#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import cv2
import numpy as np
import math


def detect_circle(image):
    """
    检测图片中的圆
    :param image:
    :return: 返回一个完全包含的圆
    """
    print(image.shape)
    height = image.shape[0]
    width = image.shape[1]

    dst = cv2.pyrMeanShiftFiltering(image, 30, 100)  # 第二个参数越大越慢

    gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
    # edges = cv2.Canny(gray, 20, 150, apertureSize=3)
    cv2.imshow("gray", gray)
    # np.uint16(width / 1.5) -
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, minDist=100, param1=100, param2=30,
                               minRadius=np.uint16(width / 4), maxRadius=np.uint16(width / 2))
    print("circles: ", circles)

    if circles is None:
        print("没有找到圆！")
        return

    circles = np.uint16(np.around(circles))

    print("总共发现%d个圆" % (len(circles[0])))

    # 获取最大半径的圆，并且都在画面之中
    target_circle = circles[0][0]
    print("target_cicle: ", target_circle)
    for circle in circles[0, :]:
        print("circle: ", circle)
        print(circle[0])
        print(circle[1])
        print(circle[2])
        if circle[2] > target_circle[2] and in_image(circle, image):
            target_circle = circle

        # cv2.circle(image, (circle[0], circle[1]), circle[2], (0, 0, 255), 5)
        # cv2.circle(image, (circle[0], circle[1]), 2, (0, 187, 247), 10)  # 画圆心

    cv2.circle(image, (target_circle[0], target_circle[1]), target_circle[2], (0, 0, 255), 5)
    cv2.circle(image, (target_circle[0], target_circle[1]), 2, (0, 187, 247), 10)  # 画圆心

    cv2.imshow("circles", image)

    return get_cicle_outer_square(target_circle), target_circle


def in_image(circle, image):
    """
    圆形是否在画面中
    :param circle:
    :param image:
    :return:
    """
    # 算出圆形外接的正方形
    square = get_cicle_outer_square(circle)
    print("shape:", image.shape)
    print("square: ", square)

    return not (square[0][0] < 0 or square[0][1] < 0 or square[1][0] > image.shape[1] or square[1][1] > image.shape[0])


def get_cicle_outer_square(cicle):
    """
    获取圆形外接正方形
    :param cicle:
    :return: [[x0, y0], [x1, y1]] 返回左上角和右下角的坐标
    """
    x0 = int(cicle[0]) - int(cicle[2])
    y0 = int(cicle[1]) - int(cicle[2])
    x1 = int(cicle[0]) + int(cicle[2])
    y1 = int(cicle[1]) + int(cicle[2])

    return [[x0, y0], [x1, y1]]


def detect_line(image, roi_rect, circle):
    """
    检测图片中的直线
    :param image:
    :return:
    """
    image = image[roi_rect[0][1]:roi_rect[1][1], roi_rect[0][0]:roi_rect[1][0]]
    cv2.imshow("lines", image)

    dst = cv2.pyrMeanShiftFiltering(image, 10, 100)  # 第二个参数越大越慢
    gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    print("半径为： ", circle[2])
    lines = cv2.HoughLines(edges, 1, np.pi / 180, int(circle[2] / 3.2))  # 最后一个参数越大，越难发现直线
    print("lines: ", lines)

    if lines is None:
        print("没有检测到直线！")
        return

    print("总共发现%d条直线" % (len(lines)))

    for line in lines:
        rho, theta = line[0]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))
        cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 2)

    # 找到2根直线的交点
    if len(lines) != 2:
        print("直线数量不是2！")
        cv2.imshow("lines", image)
        return

    cross_point = get_cross_point(lines)
    print("cross_point: ", cross_point)
    cv2.circle(image, (int(cross_point[0]), int(cross_point[1])), 2, (0, 255, 0), 2)  # 交点

    # 通过交点和圆心的直线就是目标刻度
    # 计算其角度
    # 为了直观起见，我们把这两个点连起来
    cv2.line(image, (int(cross_point[0]), int(cross_point[1])), (circle[2], circle[2]), (255, 0, 0), 2)

    cv2.imshow("lines", image)

    # 以竖直向下为0度，往左为正，一直到2pi
    # 中心点(x0, y0) 交点(x1, y1)，那么指针与竖直线的夹角等于arctan((x0-x1)/(y1-y0))
    x0 = circle[2]
    y0 = circle[2]
    x1 = cross_point[0]
    y1 = cross_point[1]
    theta = math.atan((x0 - x1) / (y1 - y0)) / (2 * math.pi) * 360

    print("theta =", theta)

    # theta的取值范围是-90~90度，theta为负的，说明指针在第2，4象限，为0地话。算出于垂直下边的夹角用|theta| * 0.00009434计算
    # 总共有265度，量程为0.25MPa，每度0.00009434Mpa
    # 如果theta

    zero_angle = 54  # 零点角度
    presure_per_degree = 0.25 / (360 - 54 * 2)
    offset_angle = 0  # 角度偏移量
    if theta > 0:
        if x0 - x1 > 0:  # 处于第一象限
            offset_angle = theta
        else:  # 处于第三象限
            offset_angle = 180 - 54 + theta
    elif theta < 0:
        if x0 - x1 > 0:  # 处于第二象限
            offset_angle = 180 - 54 + theta
        else:  # 处于第四象限
            offset_angle = 360 - 54 - theta
    else:  # 处于与垂直向上重合
        offset_angle = 180 - 54

    current_presure = presure_per_degree * offset_angle
    print("current presure: ", current_presure)

    # 调用cv.putText()添加文字
    text = "Current Presure: " + str(round(current_presure, 5))
    image = src.copy()
    cv2.putText(image, text, (20, 100), cv2.FONT_HERSHEY_COMPLEX, 2.0, (0, 0, 255), 5)
    cv2.imshow("presure", image)
    # cv2.imwrite("./presure.png", image)


def get_cross_point(lines):
    line = lines[0]
    print("第一条线", line)
    rho, theta = line[0]
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a * rho
    y0 = b * rho
    x1 = int(x0 + 1000 * (-b))
    y1 = int(y0 + 1000 * (a))
    x2 = int(x0 - 1000 * (-b))
    y2 = int(y0 - 1000 * (a))

    a1 = y1 - y2
    b1 = x2 - x1
    c1 = x1 * y2 - x2 * y1

    line = lines[1]
    print("第二条线", line)
    rho, theta = line[0]
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a * rho
    y0 = b * rho
    x1 = int(x0 + 1000 * (-b))
    y1 = int(y0 + 1000 * (a))
    x2 = int(x0 - 1000 * (-b))
    y2 = int(y0 - 1000 * (a))

    a2 = y1 - y2
    b2 = x2 - x1
    c2 = x1 * y2 - x2 * y1

    D = a1 * b2 - a2 * b1

    x = (b1 * c2 - b2 * c1) / D
    y = (a2 * c1 - a1 * c2) / D

    return [x, y]


# src = cv2.imread("./watch_small.png")
src = cv2.imread("G:/Project/raspberry-auto/equipment/data/positive/2020-17-08-25-28.jpeg")
# src = cv2.resize(src, (int(src.shape[0] / 2), int(src.shape[1] / 2)), interpolation=cv2.INTER_CUBIC)
# src = cv2.imread("./watch1.jpeg")
cv2.namedWindow("input image", cv2.WINDOW_NORMAL)
cv2.namedWindow("circles", cv2.WINDOW_NORMAL)
cv2.namedWindow("gray", cv2.WINDOW_NORMAL)
cv2.namedWindow("lines", cv2.WINDOW_NORMAL)
cv2.namedWindow("presure", cv2.WINDOW_NORMAL)
cv2.imshow("input image", src)

square, circle = detect_circle(src)
detect_line(src, square, circle)
cv2.waitKey(0)

cv2.destroyAllWindows()
