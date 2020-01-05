#!/usr/bin/env python
# coding=utf-8

from aip import AipSpeech
import os

APP_ID = '17785096'
API_KEY = 'ImMjkZ3FVClfkx6uGE4dsC3W'
SECRET_KEY = '149DmtNDzn6NGgs72i7zeOS2XSFVgEoX'

aipSpeech = AipSpeech(APP_ID, API_KEY, SECRET_KEY)


def speech(per, word):

    result = aipSpeech.synthesis(word, "zh", 1, {
        "spd": 5,
        "vol": 6,
        "per": per,
    })

    FILE = "/tmp/audio-tool.mp3"

    if not isinstance(result, dict):
        with open(FILE, 'wb') as f:
            f.write(result)

    command_str = "mplayer " + FILE
    r = os.system(command_str)

    return True
