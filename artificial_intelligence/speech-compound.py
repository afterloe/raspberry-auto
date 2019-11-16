#!/usr/bin/env python
# coding=utf-8

from aip import AipSpeech

import pygame
from time import time
import os

APP_ID='17785096'
API_KEY='ImMjkZ3FVClfkx6uGE4dsC3W'
SECRET_KEY='149DmtNDzn6NGgs72i7zeOS2XSFVgEoX'

aipSpeech = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

t1=time()
result = aipSpeech.synthesis('收到，主人', 'zh', 1, 
                             {
                                 'vol': 5,
                                 'per': 4,
                             })

if not isinstance(result, dict):
    with open('/tmp/audio.mp3', 'wb') as f:
        f.write(result)

else:
    print(result)

pygame.mixer.init()
pygame.mixer.music.load('/tmp/audio.mp3')
pygame.mixer.music.play()

t2=time()
print(t2-t1)
