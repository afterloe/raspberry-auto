#!/usr/bin/env python
# coding=utf-8

from PIL import Image
import sys

if 2 > len(sys.argv):
    print("lack arg of rgba image path")
    exit(-1)

im = Image.open(sys.argv[1])
bg = Image.new("RGB", im.size, (255, 255, 255))
bg.paste(im, im)
bg.save(sys.argv[1] + ".rgb.jpg")
