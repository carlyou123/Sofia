from judge_Command import judge_command
from STT import sound_to_text
from TTS import text_to_sound
from olami_Text import talk_to_olami

import random
import os
import time

def generate_password():
    password = ''
    password_text = ''
    for i in range(1,7):
        random_number = str(random.randrange(0,10))
        password = password + random_number + '。'
        password_text = password_text + random_number
    with open('./txt/password_Text', 'w') as f:
        f.write("这是您的验证码，请不要轻易告诉他人，这样会将您的Sofia置于危险之中。验证码： " + password_text)
    with open('./txt/password', 'w') as p:
        p.write(password_text)
    return password

def deliver_password():
    choose_number = str(random.randrange(0, 2))
    password = generate_password()
    tts_error_flag = text_to_sound(password, 'password')
    with open('./txt/master_Email','r') as f:
        email_address = f.read()
    if tts_error_flag == 1:
        os.system('mplayer ./src/tts_Error_' + choose_number + '.mp3')
    else:
        os.system('mutt -s "Sofia的密令" '+ email_address + ' -a ./sound/password.mp3< ./txt/password_Text')

def password_test():
    choose_number = str(random.randrange(0, 2))
    pass_security_flag = 0
    try:
        os.system('mplayer ./src/ding.wav')
        os.system('arecord --format=S16_LE --duration=5 --rate=16000 --file-type=wav ./sound/question.wav')
    except Exception:
        os.system('mplayer ./src/record_Error_' + choose_number + '.mp3')
        return 'Error'
    else:
        os.system('mplayer ./src/dong.wav')
        question = sound_to_text()
        with open('./txt/password', 'r') as f:
            password = f.read()
        print("password: " + password)
        print("Carl:" + question)
        if question == 'Error':
            os.system('mplayer ./src/stt_Error_' + choose_number + '.mp3')
            return 'Error'
        elif question == password:
            pass_security_flag = 1
            with open('./txt/security_Flag', 'w') as f:
                f.write(str(1))
            print('Sofia: password correct!')
            return pass_security_flag
        else:
            print('Sofia: password incorrect!')
            return pass_security_flag

def security():
    choose_number = str(random.randrange(0, 2))
    os.system('mplayer ./src/face_Please_' + choose_number + '.mp3')
    face_detact()
    with open('./txt/security_Flag', 'r') as f:
        security_flag = f.read()
    if security_flag == '1':
        os.system('mplayer ./src/face_Confirmed_' + choose_number + '.mp3')
    else:
        os.system('mplayer ./src/face_Error_' + choose_number + '.mp3')
        os.system('mplayer ./src/ask_for_password.mp3')
        try:
            os.system('mplayer ./src/ding.wav')
            os.system('arecord --format=S16_LE --duration=3 --rate=16000 --file-type=wav ./sound/question.wav')
        except Exception:
            os.system('mplayer ./src/record_Error_' + choose_number + '.mp3')
        else:
            os.system('mplayer ./src/dong.wav')
            question = sound_to_text()
            print("Carl:" + question)
            if question == 'Error':
                os.system('mplayer ./src/stt_Error_' + choose_number + '.mp3')
            elif question == '好的' or question == '可以' or question == '好' or question == '是' or question == '行':
                deliver_password()
                os.system('mplayer ./src/speak_After_Ding.mp3')
                time.sleep(30)
                pass_security_flag = password_test()
                if pass_security_flag == 1:
                    os.system('mplayer ./src/password_Confirmed_' + choose_number + '.mp3')
                elif pass_security_flag == 0:
                    os.system('mplayer ./src/password_Error_' + choose_number + '.mp3')
                else:
                    pass
            else:
                os.system('mplayer ./src/password_Unwanted.mp3')



if __name__=='__main__':
    already_import_facedetect_flag = 0
    public_flag = 0
    face_detect_count = 0
    with open('./txt/loop_Count','r') as f:
        loop_count = int(f.read())
    with open('./txt/security_Flag','r') as f:
        security_flag = f.read()
    if security_flag == '0':
        from security_Face_Detact import face_detact
        already_import_facedetect_flag = 1
    else:
        pass

    while True:
        choose_number = str(random.randrange(0, 2))
        loop_count += 1
        print(loop_count)
        if loop_count == 50:
            loop_count = 0
            with open('./txt/security_Flag', 'w') as f:
                f.write(str(0))
            with open('./txt/loop_Count', 'w') as f:
                f.write(str(0))
        if loop_count%5 == 0:
            with open('./txt/loop_Count', 'w') as f:
                f.write(str(loop_count))
        if face_detect_count == 3:
            break
        with open('./txt/security_Flag', 'r') as f:
            security_flag = f.read()
        try:
            if public_flag == 0:
                print('I\'m Sofia! You can talk to me~')
                os.system('python listen/sofia.py listen/resources/sofia.pmdl > /dev/null 2>&1')
            else:
                print('I\'m Alexa! You can talk to me~')
                os.system('python listen/sofia.py listen/resources/alexa.umdl > /dev/null 2>&1')
            if security_flag == '0':
                if already_import_facedetect_flag == 1:
                    face_detect_count += 1
                    security()
                else:
                    from security_Face_Detact import face_detact
                    already_import_facedetect_flag = 1
                    face_detect_count += 1
                    security()
            elif security_flag == '1':
                try:
                    os.system('arecord --format=S16_LE --duration=3 --rate=16000 --file-type=wav ./sound/question.wav')
                except Exception:
                    os.system('mplayer ./src/record_Error_' + choose_number + '.mp3')
                else:
                    os.system('mplayer ./src/dong.wav')
                    question = sound_to_text()
                    if question == 'Error':
                        os.system('mplayer ./src/stt_Error_' + choose_number + '.mp3')
                    elif question == 'jump':
                        continue
                    else:
                        print("Carl:"+question)
                        command_flag = judge_command(question)
                        if command_flag == 0:
                            response = talk_to_olami(question)
                            if response == "Error":
                                os.system('mplayer ./src/turing_Error_' + choose_number + '.mp3')
                                break
                            elif response == "Format":
                                os.system('mplayer ./src/turing_Format_' + choose_number + '.mp3')
                                continue
                            else:
                                print("Sofia:"+response)
                                tts_error_flag = text_to_sound(response, 'response')
                                if tts_error_flag == 1:
                                    os.system('mplayer ./src/tts_Error_' + choose_number + '.mp3')
                                else:
                                    os.system('mplayer ./sound/response.mp3')
                        elif command_flag == "jump":
                            os.system('mplayer ./src/bye_' + choose_number + '.mp3')
                            break
                        elif command_flag == "public":
                            public_flag = 1
                        elif command_flag == "private":
                            public_flag = 0
                        elif command_flag == 'left':
                            loop_count = 0
                            os.system('echo -n "0" > ./txt/security_Flag')
                            os.system('echo -n "0" > ./txt/loop_Count')
                        else:
                            continue
            else:
                break
        except Exception:
            os.system('mplayer ./src/fatal_Error_' + choose_number + '.mp3')
            break
