# coding=utf-8
import sys
import json

from urllib.request import urlopen
from urllib.request import Request
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.parse import quote_plus

def text_to_sound(RESPONSE, path_name):

    # 发音人选择, 0为普通女声，1为普通男生，3为情感合成-度逍遥，4为情感合成-度丫丫，默认为普通女声
    PER = 0
    # 语速，取值0-15，默认为5中语速
    SPD = 6
    # 音调，取值0-15，默认为5中语调
    PIT = 6
    # 音量，取值0-9，默认为5中音量
    VOL = 7
    # 下载的文件格式, 3：mp3(default) 4： pcm-16k 5： pcm-8k 6. wav
    AUE = 3

    FORMATS = {3: "mp3", 4: "pcm", 5: "pcm", 6: "wav"}
    FORMAT = FORMATS[AUE]
    CUID = "123456PYTHON"
    TTS_URL = 'http://tsn.baidu.com/text2audio'
    tts_error_flag = 0

    with open("./txt/token.txt","r") as re:
        token = re.read()
    tex = quote_plus(RESPONSE)
    params = {'tok': token, 'tex': tex, 'per': PER, 'spd': SPD, 'pit': PIT, 'vol': VOL, 'aue': AUE, 'cuid': CUID,
              'lan': 'zh', 'ctp': 1}  # lan ctp 固定参数

    data = urlencode(params)

    req = Request(TTS_URL, data.encode('utf-8'))
    try:
        f = urlopen(req)
        result_str = f.read()
    except  URLError:
        print('Error')
        tts_error_flag = 1
        return tts_error_flag
    else:
        save_file = path_name + '.' + FORMAT
        with open("./sound/"+save_file, 'wb') as of:
            of.write(result_str)
        return tts_error_flag


if __name__ == '__main__':
    text_to_sound("1。2。3。4。5。6。", 'password')
