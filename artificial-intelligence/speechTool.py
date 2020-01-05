#!/usr/bin/env python
# coding=utf-8

import argparse

from aip import AipSpeech
import os

def init():
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "-per", type=int, help="情感和成人 3, 4")
    ap.add_argument("-t", "-text", help="朗读文字")
    args = vars(ap.parse_args())
    return args

APP_ID = '17785096'
API_KEY = 'ImMjkZ3FVClfkx6uGE4dsC3W'
SECRET_KEY = '149DmtNDzn6NGgs72i7zeOS2XSFVgEoX'

aipSpeech = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

arg_map = init()
result = aipSpeech.synthesis(arg_map["t"], "zh", 1, {
    "spd": 5,
    "vol": 6,
    "per": arg_map["p"],
})

FILE = "/tmp/audio-tool.mp3"

if not isinstance(result, dict):
    with open(FILE, 'wb') as f:
        f.write(result)

command_str = "mplayer " + FILE
r = os.system(command_str)
