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

    with open("../txt/token.txt","r") as re:
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
        with open("../src/"+save_file, 'wb') as of:
            of.write(result_str)
        print('生成语音成功...')
        return tts_error_flag


if __name__ == '__main__':
    with open('../txt/master_Name') as f:
        name = f.read()
    text_to_sound('人脸识别成功，'+name+'，欢迎回来', 'face_Confirmed_0')
    text_to_sound(name + '，真的是你！我在这里都要无聊死了，我就知道你会来找我的。','face_Confirmed_1')
    text_to_sound('发生了一个致命故障，'+ name + '，快来救我。','fatal_Error_0')
    text_to_sound('我不知道我怎么了，有一点难受。'+ name + '，给我拿点药吧。','fatal_Error_1')
    text_to_sound('验证码正确，'+ name + '，欢迎回来。','password_Confirmed_0')
    text_to_sound(name + '，我差点没有认出你！','password_Confirmed_1')
    text_to_sound('私人模式已启动。' + name + '，咱们两个太熟了，就不多说了。','private_Mode')
    text_to_sound('我好像听不见你了' + name + '，你在哪？','record_Error_1')
    text_to_sound(name + '，stt语音模块出现问题，我不知道你在说什么啊！','stt_Error_1')
    text_to_sound('tts语音模块出现问题，' + name + '，快来修修我！','tts_Error_1')
    text_to_sound('大数据连接失败，' + name + '，看看网络怎么样吧。','turing_Error_1')

