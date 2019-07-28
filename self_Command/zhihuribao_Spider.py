#coding:utf-8
from TTS import text_to_sound
from STT import sound_to_text

import os
import re
import subprocess
import random
import requests
#import lxml
import json
from bs4 import BeautifulSoup

def get_title_list():
    web_error_flag = 0
    NEWS_URL = "https://news-at.zhihu.com/api/4/news/latest"

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
    try:
        web_data = requests.get(NEWS_URL, headers = headers)
    except Exception:
        web_error_flag = 1
        return web_error_flag
    else:
        data = json.loads(web_data.text)
        return data

def process_title_list(data, stories_length, top_stories_length):

    sentence = '欢迎收听最新的知乎日报，您可以选择想要收听的文章序号，下面是具体内容。首先是普通故事。'
    for i in range(0, stories_length):
        sentence += '第' + str(i + 1) + '篇:' + data['stories'][i]['title'] + '。'
    sentence += '接下来是首选故事。'
    for i in range(stories_length, stories_length + top_stories_length):
        sentence += '第' + str(i + 1) + '篇:' + data['top_stories'][i-stories_length]['title'] + '。'
    sentence += '您想收听哪一篇文章主题呢？请说出它的序号。'
    return sentence

def get_content(id):
    CONTENT_URL = 'http://daily.zhihu.com/story/' + str(id)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
    try:
        content = requests.get(CONTENT_URL, headers=headers).text
    except Exception:
        web_error_flag = 1
        return web_error_flag
    else:
        return content

def process_content(content):
    soup = BeautifulSoup(content, 'lxml')
    answer = soup.find_all('div', class_='answer')
    title = soup.find('div', class_='headline').find('div').find('h1', class_='headline-title').text
    authors = []
    bios = []
    articles = []
    if len(answer) == 0:
        return '抱歉，此篇文章为外部链接，无法有效读取。'
    else:
        pass
    for i in range(0,len(answer)):
        authors.append(answer[i].find('div', class_='meta').find('span', class_='author').text)
    for i in range(0,len(answer)):
        bios.append(answer[i].find('div', class_='meta').find('span', class_='bio').text)
    for i in range(0,len(answer)):
        para = answer[i].find('div', class_='content').find_all('p')
        article = ''
        for j in range(0, len(para)):
            article +=  para[j].text
        articles.append(article)

    sentence = '您所选择的主题文章已获取，一共有' + str(len(answer)) + '篇，下面进行播报。主题为：' + title + '。'
    for i in range(0, len(answer)):
        sentence += '第' + str(i+1) + '篇。作者：' + authors[i] + '。作者介绍：' + bios[i] + '。正文：' + articles[i] + '。'
    sentence += '知乎日报播送完毕。'
    print(sentence)
    return sentence


if __name__ == '__main__':
    choose_number = str(random.randrange(0,2))
    title_list = get_title_list()
    if title_list == 1:
        os.system('mplayer ../src/network_Error.mp3')
        exit()
    else:
        pass
    stories_length = len(title_list['stories'])
    top_stories_length = len(title_list['top_stories'])
    zhihu_title = process_title_list(title_list, stories_length, top_stories_length)
    print(zhihu_title)

    tts_error_flag = text_to_sound(zhihu_title, 'zhihu_Title')
    if tts_error_flag == 1:
        os.system('mplayer ../src/tts_Error_' + choose_number + '.mp3')
        exit()
    else:
        os.system('mplayer ../sound/zhihu_Title.mp3')
    try:
        os.system('mplayer ../src/ding.wav')
        os.system('arecord --format=S16_LE --duration=3 --rate=16000 --file-type=wav ../sound/question.wav')
    except Exception:
        os.system('mplayer ../src/record_Error_' + choose_number + '.mp3')
        exit()
    else:
        os.system('mplayer ../src/dong.wav')
        title_number = sound_to_text()
        print('Carl: '+ title_number)
        cn_sum = {'一': '1', '二': '2', '三': '3', '四': '4', '五': '5', '六': '6', '七': '7', '八': '8', '吧':'8', '九': '9', '零': '0',
                  '十': 10}
        if title_number == 'Error':
            os.system('mplayer ./src/stt_Error_' + choose_number + '.mp3')
            exit()
        elif title_number == 'jump':
            os.system('mplayer ../src/did_not_speak.mp3')
            exit()
        elif title_number in cn_sum:
            title_digit_number = cn_sum[title_number]
            print(title_digit_number)
            if title_digit_number.isdigit():
                title_number = int(title_digit_number)
                if title_number > 0 and title_number <= stories_length:
                    id = title_list['stories'][title_number-1]['id']
                elif title_number > stories_length and title_number < stories_length + top_stories_length:
                    id = title_list['top_stories'][title_number - stories_length - 1]['id']
                else:
                    os.system('mplayer ../src/zhihu_Number_Error.mp3')
                    exit()
                print('id: '+str(id))
                content = get_content(id)
                if content == 1:
                    os.system('mplayer ../src/network_Error.mp3')
                    exit()
                else:
                    zhihu_articles = process_content(content)
                    articles_split = re.findall(r'.{300}', zhihu_articles)
                    articles_split.append(zhihu_articles[len(articles_split)*300:])
                    for i in range(0, len(articles_split)):
                        tts_error_flag = text_to_sound(articles_split[i], 'zhihu_Articles_' + str(i))
                        if tts_error_flag == 1:
                            os.system('mplayer ../src/tts_Error_' + choose_number + '.mp3')
                            exit()
                        else:
                            pass

                    print(len(articles_split))
                    for j in range(0, len(articles_split)):
                        os.system('mplayer ../sound/zhihu_Articles_' + str(j) +'.mp3')
                    exit()
            else:
                os.system('mplayer ../src/zhihu_Number_Error.mp3')
                exit()
        else:
            os.system('mplayer ../src/zhihu_Number_Error.mp3')
            exit()



