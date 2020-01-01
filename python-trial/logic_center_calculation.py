#!/usr/bin/env python
# coding=utf-8

import math
import numpy as np

zero_width = 640 / 2
zero_hight = 480 / 2
max_c = math.sqrt(math.pow(zero_width, 2) + math.pow(zero_hight, 2))

p_x = np.random.randint(0, 640)
p_y = np.random.randint(0, 480)
print("point(%d, %d)" % (p_x, p_y))

a = math.pow((p_x - zero_width), 2)
b = math.pow((p_y - zero_hight), 2)
c = math.sqrt(a + b)
print("a = %d, b = %d, c = %.3f" % (a, b, c))
print("max c is %.3f" % (max_c))


