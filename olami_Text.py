# -*-coding=utf-8-*-
import requests
import time
import hashlib
import os

def md5(md5_src):
    sign = hashlib.md5()
    sign.update(md5_src.encode('utf-8'))
    return sign.hexdigest()

def talk_to_olami(msg):
    KEY = '7685f7ea8359419888b7aee81894b405'
    API_URL = "http://cn.olami.ai/cloudservice/api"
    timestamp = str(int(time.time())) + '000'
    md5_src = 'a0f543efd22a4e78b3d95a213d02c5a1api=nliappkey=7685f7ea8359419888b7aee81894b405timestamp=' + timestamp + 'a0f543efd22a4e78b3d95a213d02c5a1'
    sign = md5(md5_src)
    final_url = API_URL
    final_url += '?appkey='+ KEY
    final_url += '&api=nli'
    final_url += '&timestamp=' + timestamp
    final_url += '&sign=' + sign
    final_url += '&rq={\'data\':{\'input_type\':1,\'text\':\'' + msg + '\','
    final_url += '\'location\':{\'longitude\':\'108000000\',\'latitude\':\'34000000\'}},'
    final_url += '\'data_type\':\'stt\',\'nli_config\':{\'slotname\':\'photographer\'}}&cusid=sofia'


    try:
        response = requests.post(final_url).json()
        type = response.get('data').get('nli')[0].get('type')
        answer = response.get('data').get('nli')[0].get('desc_obj').get('result') + '。'
        if type == 'selection':
            length = len(response.get('data').get('nli')[0].get('data_obj'))
            desc_type = response.get('data').get('nli')[0].get('desc_obj').get('type')
            if desc_type == 'poem':
                for i in range(0, length):
                    answer += '第' + str(i+1) + '首：'
                    answer += response.get('data').get('nli')[0].get('data_obj')[i].get('poem_name') + '，'
                    answer += '作者：'
                    answer += response.get('data').get('nli')[0].get('data_obj')[i].get('author') + '。'
            if desc_type == 'cooking':
                for i in range(0, length):
                    answer += response.get('data').get('nli')[0].get('data_obj')[i].get('name') + '。'
        elif type == 'joke':
            answer += response.get('data').get('nli')[0].get('data_obj')[0].get('content')
        elif type == 'cooking':
            answer += '对了，菜单已经发送到你的邮箱了哦~'
            answer += response.get('data').get('nli')[0].get('data_obj')[0].get('content')
            with open('./txt/cook_Menu', 'w') as f:
                f.write(answer)
            with open('./txt/master_Email', 'r') as f:
                email_address = f.read()
            os.system('mutt -s "你要的菜谱已经呈上，快来试试吧~" ' + email_address + ' < ./txt/cook_Menu')
        elif type == 'baike':
            answer += response.get('data').get('nli')[0].get('data_obj')[0].get('description')
        elif type == 'tvprogram':
            length = len(response.get('data').get('nli')[0].get('data_obj'))
            for i in range(0,length):
                answer += response.get('data').get('nli')[0].get('data_obj')[i].get('time') + '，'
                answer += response.get('data').get('nli')[0].get('data_obj')[i].get('name') + '。'
        elif type == 'ds':
            olami_flag = "Format"
            return olami_flag
        else:
            pass
        if answer == '':
            answer = '咦，我感觉我的思维出现了一些问题。'
        return answer
    except Exception:
        olami_flag = "Error"
        return olami_flag


if __name__=='__main__':
    print(talk_to_olami("1564算24点"))
