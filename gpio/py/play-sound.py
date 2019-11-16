#!/usr/bin/env python
# coding=utf-8

from pygame import mixer
import time

mixer.init()
mixer.music.load('/tmp/audio.mp3')
mixer.music.play(1, 0.0)
mixer.music.stop()
