import cv2
import sys
import numpy as np


if 1 > len(sys.argv):
    print("missing arg")
    exit(-1)

img = cv2.imread(sys.argv[1])
cv2.imshow("Image", img)
cv2.waitKey(0)

cv2.destroyAllWindows()
