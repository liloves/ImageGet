#-*- coding: UTF-8 -*-

# 使用说明
# 1.使用管理员模式

import os

python_path = "C:\Program Files\Python27\Scripts"
target_path = "E:\Code\ImageGet\ImageGet\ImageGet\Source\ImageGet.py"

# 使用pyinstaller工具发布win应用
# using pyinstaller tool to release windows application
# 使用命令行工具配置目标python文件并执行pyinstaller转化应用
cmd = r'"C:\Program Files\Python27\Scripts\pyinstaller.exe" -F -w "E:\Code\ImageGet\ImageGet\ImageGet\Source\ImageGet.py"'

print cmd
os.system(cmd)

# created path includes excuted program for windows
dictpath = "C:\Program Files\Python27\Scripts"

os.startfile(dictpath)
