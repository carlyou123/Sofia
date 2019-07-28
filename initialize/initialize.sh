#!/bin/bash

echo -e "\033[35m~欢迎使用此初始化脚本~\n------------------------------\n###版权所有###\nAuthor: Carl Yau\nWebsite: www.elapse.life\n------------------------------\n\033[0m"
echo -e "\033[35m想要使用本语音助手，您需要将脸部识别模型、声纹模型导入，并留下您的名字和邮箱。\n不要忘了每个月对百度的token进行刷新（您可以通过crontab -e命令自动化执行）。\n哦，对了，初始的语音助手中采用的百度和OLAMI的KEY全部为作者私人应用的，故不保证会一直有效。强烈建议您将python文件中的KEY改为自己创建应用的KEY。\n请阅读README文件中的相关内容。您也可以在作者的个人网站中找到关于此语音助手的更为详细的介绍和使用方法。\n祝您玩得愉快~比心\n\033[0m"
echo -e "\033[35m下面请选择你想要执行的选项的序号：\n1. 初始化个人信息录入（您的名字和邮箱等信息）\n2. 百度语音token刷新（请在每月刷新一次）\n3. 退出\n\033[0m"
read choice
case $choice in
	1)
		echo -e "欢迎进行个人信息录入\n请输入您的名字，您希望您的助手称呼您什么？"
		read name
		echo -n $name > ../txt/master_Name
		echo "很好，现在请输入您的邮箱地址（请注意拼写正确）~"
		read email
		echo -n $email > ../txt/master_Email
		echo "正在生成语音文件，请稍后......"
		python3 ./generate_Source_Sound.py
		echo "Good job!初始化已完成。现在您可以使用您的助手了~";;
	2)
		python3 ./fetch_Baidu_Token.py
		echo "已尝试获取token...";;
	3)
		echo "正在退出...";;
	*)
		echo "该选项不存在！"
		exit 1;;
esac
exit 0
