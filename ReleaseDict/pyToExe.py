# coding:utf-8
import os

pyinstPath = u'\"C:\Program Files\Python27\Scripts'
print pyinstPath
pyinstLocation = pyinstPath + '\\' + u'pyinstaller.exe' + u'\"'
print pyinstLocation

command1 = u' -F ' + u' -w '

path = r'C:\Users\Administrator\Desktop'
targPath = u'C:\\Users\Administrator\Desktop' +  u'\\' + u'IpSwitch.py'


import Tkinter

cmd = pyinstLocation + command1 + targPath

print cmd

getinfo = input('输入Y执行:\n')
if getinfo == 'Y' or getinfo == 'y' : 
    print os.system(cmd)



if __name__ == '__main__':
    print 1




