#!/usr/bin/env python
# coding=utf-8

from aip import AipSpeech
import json

APP_ID='17785096'
API_KEY='ImMjkZ3FVClfkx6uGE4dsC3W'
SECRET_KEY='149DmtNDzn6NGgs72i7zeOS2XSFVgEoX'

aipSpeech = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

FILE='/home/pi/20191116_160931.m4a'

result = aipSpeech.asr(get_file_content(FILE), 'm4a', 16000, 
                       {
                           'dev_pid': 1536,
                       })

print(result['result'][0])

result = json.dumps(result)
print(result)
