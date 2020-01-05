#!/usr/bin/env python
# coding=utf-8

from aip import AipSpeech
from time import time
import os

APP_ID='17785096'
API_KEY='ImMjkZ3FVClfkx6uGE4dsC3W'
SECRET_KEY='149DmtNDzn6NGgs72i7zeOS2XSFVgEoX'

aipSpeech = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

t1=time()
result = aipSpeech.synthesis('好的, 命令收到。云台即将调整完毕', 'zh', 1, 
                             {
                                 'spd': 5,
                                 'vol': 5,
                                 'per': 3,
                             })

FILE = '/tmp/audio-1.mp3'

if not isinstance(result, dict):
    with open(FILE, 'wb') as f:
        f.write(result)

else:
    print(result)

command_str = 'mplayer ' + FILE
r = os.system(command_str)

t2=time()
print(t2-t1)
print(r)
