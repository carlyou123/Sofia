import os

def judge_command(command):
    command_flag = 1

    if command == "开启公共模式":
        command_flag = "public"
        os.system('mplayer ./src/public_Mode.mp3')
        return command_flag
    elif command == "开启私人模式":
        command_flag = "private"
        #hotword: alexa
        os.system('mplayer ./src/private_Mode.mp3')
        return command_flag
    elif command == "知乎日报":
        os.system('cd ./self_Command&&python3 ./zhihuribao_Spider.py')
    elif command == "放战歌":
        os.system('mplayer ./src/play_Battle_Song.mp3')
        os.system('mplayer ./src/music/the_Avengers.mp3')
    elif command == "开灯":
        os.system('python3 ./iot/light_On.py')
    elif command == "关灯":
        os.system('python3 ./iot/light_Off.py')
    elif command == "自拍":
        with open('./txt/master_Email', 'r') as f:
            email_address = f.read()
        os.system('raspistill -o ~/my_Photo/selfie.jpg&&convert ~/my_Photo/selfie.jpg -quality 50 ~/my_Photo/selfie.jpeg&&mutt -s "这是你美美的自拍" ' + email_address + ' -a ~/my_Photo/selfie.jpeg')
        os.system('mplayer ./src/selfie.mp3')
    elif command == "关机":
        os.system('sudo shutdown now')
    elif command == "重启":
        os.system('sudo reboot now')
    elif command == "开启离开模式":
        command_flag = "left"
        os.system('mplayer ./src/leave_Mode.mp3')
    elif command == "再见":
        command_flag = "jump"
        return command_flag
    else:
        command_flag = 0

    return command_flag
