# coding:utf-8

import os
import urllib2
import mysql
from Tkinter import *

class dataServe:

    def __init__(self):

        self.loginID = 'admin'
        self.loginCode = '1234'

        self.sqlObj = mysql()

class Widget:

    def __init__(self):

        self.widget = Tk()
        #self.widget.geometry('500x300+500+200')

        # ip address
        self.ipAddr = StringVar(value = '192.168.1.10')
        self.ipEnter = Entry(self.widget,textvariable  = self.ipAddr)
        self.ipEnter.grid(row = 1,column = 0,sticky = 'snew')

        # 子网掩码
        self.mask = StringVar(value = '255.255.255.0')
        self.maskEnter = Entry(self.widget,textvariable  = self.mask)
        self.maskEnter.grid(row = 2,column = 0,sticky = 'snew')

        # 网关
        self.gate = StringVar(value = '192.168.1.1')
        self.gateEnter = Entry(self.widget,textvariable  = self.mask)
        self.gateEnter.grid(row = 3,column = 0,sticky = 'snew')

        # DNS
        self.dnsAddr = StringVar(value = '192.168.1.1')
        self.dnsEnter = Entry(self.widget,textvariable  = self.dnsAddr)
        self.dnsEnter.grid(row = 4,column = 0,sticky = 'snew')


        self.radioFrame = Frame(self.widget)
        self.radioFrame.grid(row = 0,column = 0,sticky = 'snew')
        
        self.var = IntVar()
        self.checkButton1 = R1 = Radiobutton(self.radioFrame, text=u"DHCP", \
                          variable=self.var, value=1, command = self.chageMode)
        self.checkButton1.grid(row = 0,column = 0,sticky = 'snew')
        self.checkButton2 = R1 = Radiobutton(self.radioFrame, text=u"固定IP", \
                          variable=self.var, value=2, command = self.chageMode)
        self.checkButton2.grid(row = 0,column = 1,sticky = 'snew')
        
        self.widget.mainloop()

    def chageMode(self):
        if self.var.get() == 1:
            DHCPcmd = \
u'''netsh interface ip set address name = "以太网" source = dhcp 
netsh interface ip set dns "以太网" source = dhcp
'''            
            print DHCPcmd
            print os.system(DHCPcmd.encode('GBK'))
        elif self.var.get() == 2:
            conIP = self.ipEnter.get()
            print type(conIP)
            conIPcmd = \
u'''Netsh interface IP Set Addr "以太网" Static ''' + \
conIP + u''' 255.255.255.0 192.168.22.1 1
Netsh interface IP Set dns "以太网" static 192.168.22.1 primary
pause'''
            print conIPcmd
            print os.system(conIPcmd.encode('GBK'))

if __name__ == '__main__':
    
    widgetObj = Widget()

