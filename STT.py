# coding=utf-8

import os
import sys
import json
import time

from urllib.request import urlopen
from urllib.request import Request
from urllib.error import URLError
from urllib.parse import urlencode

timer = time.perf_counter

def sound_to_text():
    stt_error_flag = 0
    AUDIO_FILE = './sound/question.wav'  # 只支持 pcm/wav/amr
    FORMAT = AUDIO_FILE[-3:];  # 文件后缀只支持 pcm/wav/amr

    CUID = '123456PYTHON';
    RATE = 16000;

    DEV_PID = 1536;  # 1537 表示识别普通话，使用输入法模型。1536表示识别普通话，使用搜索模型。根据文档填写PID，选择语言及识别模型
    ASR_URL = 'http://vop.baidu.com/server_api'

    with open("./txt/token.txt","r") as re:
        token = re.read()
    speech_data = []
    with open(AUDIO_FILE, 'rb') as speech_file:
        speech_data = speech_file.read()
    length = len(speech_data)
    if length == 0:
        raise DemoError('file %s length read 0 bytes' % AUDIO_FILE)

    params = {'cuid': CUID, 'token': token, 'dev_pid': DEV_PID}
    params_query = urlencode(params);

    headers = {
        'Content-Type': 'audio/' + FORMAT + '; rate=' + str(RATE),
        'Content-Length': length
    }

    url = ASR_URL + "?" + params_query
    req = Request(ASR_URL + "?" + params_query, speech_data, headers)
    try:
        f = urlopen(req)
        result_str = f.read()
    except  URLError as err:
        print('asr http response http code : ' + str(err.code))
        result_str = err.read()
        stt_error_flag = 'Error'
        return stt_error_flag
    else:
        result_str = eval(str(result_str, 'utf-8'))
        try:
            result = result_str['result'][0]
            return result
        except Exception:
            os.system('mplayer ./src/did_not_speak.mp3')
            return 'jump'


if __name__=='__main__':
    text = sound_to_text()
    print(text)
