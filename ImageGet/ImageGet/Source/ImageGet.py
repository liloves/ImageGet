#-*- coding: UTF-8 -*-

'''
Author: Li Geng
Meaning: App, Image get
Description: Use various module to complete the Web Detect with UI form
             if you know the http website, type it into dialog for customing to
             set the website address and smell the files in HTML
'''

import urllib
import re
import os

from Tkinter import *
import tkFileDialog
import threading

import zlib
from HTMLParser import HTMLParser
from cStringIO import StringIO
from urlparse import urljoin, urlparse



'''
用于匹配正则式,返回匹配结果
用法regFind(表达式,文本内容)
'''
def regFind(reg,text):
    pattern  =  re.compile(reg)
    return re.findall(pattern,text)


'''用于获取html源,返回对应文本内容'''
def getHtml(url):
    fp = urllib.urlopen(url)
    if fp.getcode() == 200:
        bytesText = fp.read()
        if fp.headers.get('content-encoding') == 'gzip':
            return zlib.decompress(bytesText, 16+zlib.MAX_WBITS)
        else:
            return bytesText
    elif fp.getcode() == 404:
        print u'网址未找到'
        return ''

    
'''
保存图片列表至对应路径
用法saveGraph(路径,图片url列表)
'''
def saveGraph(readyPath,imglist):
    x = 0
    for imgurl in imglist:
        try:
            urllib.urlretrieve(imgurl, readyPath + '/%s.jpg' % x)
            x += 1
        except Exception,e:
            print e
            return 0
    return x
        

def getImg(html, IOobj, rootPath):
    imglist = regFind(r'<img.*?src="(.+?\.jpg)".*?>',html)   #解析图像列表
    titlelist = regFind(r'<head>[\s\S]*<title>([\s\S]*)</title>[\s\S]*</head>',html)
    htmlTitle = titlelist[0].decode('GBK')       #从list中提取出title的字符串变量,并解码为unicode
    htmlTitleUTF8 = htmlTitle.encode('utf-8')
    IOobj.addMessage(htmlTitleUTF8 + '>>>' + "共有" + str(len(imglist)) + "张图片\n")
    readyPath = rootPath + '/' + htmlTitle
    x = 0                          # 图片计数器
    if not (os.path.exists(readyPath) and len(os.listdir(readyPath)) == len(imglist) ):
        # 如果不同时满足(文件夹存在和图片下载完整)则需要新下载所有内容
        # 尝试创建目录
        if not os.path.exists(readyPath):
            try:
                os.mkdir(readyPath)
            except Exception,e:
                print "文件夹创建异常:",htmlTitle,Exception,":",e  # 防止新建文件夹异常
        # 录建立后下载图片
        if os.path.exists(readyPath):
            x = saveGraph(readyPath,imglist)
    printContext = htmlTitleUTF8 + ">>>获取图片" + str(x) + "张\n"
    IOobj.addMessage(printContext)    # 引用了控件对象



# HTML Parser to locate the tag of charset
class AnchorParser(HTMLParser):
        
    def handle_starttag(self, tag, attrs):
        self.tag_name = 'meta'
        self.tag_context = 'charset'
        if tag != self.tag_name:
            return
        print tag
        print attrs
        if not hasattr(self, 'data'):
            self.data = []
        for attr in attrs:
            if attr[0] == self.tag_context:
                self.data.append(attr[1])

    def getLink(self, webAddr):
        HtmlText = getHtml(webAddr)
        self.feed(HtmlText)
        AddrGroup = []
        for x in self.data:
            AddrGroup.append(urljoin(webAddr,x))
        return AddrGroup

 
# Main Widget class for showing the UI
class Widget():
    
    def __init__(self):

        # tkinter main
        self.root = Tk()
        self.root.minsize(400, 200)
        self.root.title("Get Image Serve")

        # menu
        self.menuInit()

        # active elements
        self.butnForm = Frame()
        self.btn1 = Button(self.butnForm,text = "载入地址",command = self.btn1Clicked).pack(expand=YES, fill="both")
        self.btn2 = Button(self.butnForm,text = "下载",command = self.btn2Clicked).pack(expand=YES, fill="both")
        self.btn3 = Button(self.butnForm,text = "保存地址",command = self.btn3Clicked).pack(expand=YES, fill="both")
        self.ety1 = Entry(self.root)
        self.txt1= Text(self.root)
        self.txt1.bind("<KeyPress>", lambda e : "break")

        ## pack
        self.butnForm.grid(row=0, column=0, sticky=W)
        self.ety1.grid(row=0, column=1, sticky=W)
        self.txt1.grid(row=2, column=0, columnspan=10, rowspan=3)

        # var
        self.nonFlag = 0            # 配置标记：1,空配置;0,有配置
        self.threadpool = []        # 线程池

        # director check
        self.checkDirectory()
        
    def menuInit(self):
        # main menu
        menubar = Menu(self.root)
        # child menu
        filemenu = Menu(menubar, tearoff = 0)  
        filemenu.add_command(label = "显示当前地址", command = self.showWebAddr)
        filemenu.add_separator()  
        filemenu.add_command(label = "退出", command = self.root.quit)
        menubar.add_cascade(label = "开始", menu = filemenu)
        # child menu
        filemenu = Menu(menubar, tearoff=0)  
        filemenu.add_command(label = "设置存储文件夹", command = self.directoryConfig)
        filemenu.add_command(label = "重新加载配置文件", command = self.loadConfig)
        filemenu.add_separator()  
        filemenu.add_command(label = "设置爬虫")  
        menubar.add_cascade(label = "参数配置", menu = filemenu) 
        # link
        self.root.config(menu=menubar)

    def showWebAddr(self):
        if self.webAddr == '':
            self.addMessage('目标地址为空\n')
        else:
            self.addMessage('设置地址为'+ self.webAddr + '\n')
    
    def btn1Clicked(self):
        if self.ety1.get() != '':
            self.webAddr = self.ety1.get()
            self.addMessage('设置地址为:'+self.webAddr + '\n')
        else:
            self.addMessage('设置地址为空\n')

    def btn2Clicked(self):
        if self.webAddr == '' :
            self.addMessage('目前没有读到上次结束的地址,请输入一个网址\n')
        else:
            try:
                thisThread = threading.Thread(target=self.webDetect,args=(self.webAddr,self))
                thisThread.start()
            except Exception,e:
                print '线程创建或启动异常:',Exception,':',e

    def btn3Clicked(self):
        self.addMessage('保存地址为:'+self.webAddr + '\n')
        cfgObj = Config()
        cfgObj.SaveConfig(self.webAddr)
    
    def mainloop(self):
        self.root.mainloop()

    def webDetect(self,webAddr,IOobj):
        IOobj.addMessage('加载地址:' + webAddr + '\n')
        htmlText = getHtml(webAddr)
        thisThread = threading.Thread(target=getImg,args=(htmlText, IOobj, self.rootPath))
        thisThread.start()
        GraspList = regFind(r'<a href=(.+?\.html)>.*?</a>',htmlText)
        try :
            self.webAddr =  'http://' + urlparse(webAddr).netloc + GraspList[1]    #爬虫目标地址
        except Exception,e:
            print '爬虫问题',Exception,':',e
            return 'http://' + urlparse(webAddr).netloc + GraspList[0]    #爬虫目标地址
    
    def addMessage(self,text):
        self.txt1.insert(0.0,text)

    def checkDirectory(self):
        self.rootPath = './GraphFile'    # 默认保存位置
        if not os.path.exists(self.rootPath):
            self.addMessage('目前未设定保存文件夹,请指定一个保存地址\n')
            self.directoryConfig()
        self.loadConfig()

    def loadConfig(self):
        # 读取历史配置
        self.iniFile = 'store_html.ini'
        self.ConfigObj = Config(self.rootPath + '/'+ self.iniFile)         #配置文件
        self.webAddr = self.ConfigObj.LoadConfig()  #加载保存的地址
        if self.webAddr == '':
            self.nonFlag = 1
            self.addMessage('目前没有读到上次结束的地址,请输入一个网址\n')
        else:
            self.addMessage('上次结束的地址为:' + self.webAddr + '\n')

    def directoryConfig(self):
        getPath =  \
            tkFileDialog.askdirectory(parent=self.root,initialdir="/",  \
            title='选取保存内容的文件夹')
        if getPath != '':
            self.addMessage(u'设置目录为: ' + getPath + u'\n')
            self.rootPath = getPath
        else:
            self.addMessage(u'未设置目录\n')
            #self.addMessage(u'未设置目录，将使用默认路径: ' + self.rootPath + u'\n')
            #if not os.path.exists(self.rootPath):
                #os.mkdir(self.rootPath)    # 未存在默认目录需要创建
            

# configuration file save & load
class Config():
    def __init__(self,configFileName = 'store_html.ini'):
        self.configFileName = configFileName
    
    def LoadConfig(self):
        if not os.path.exists(self.configFileName):
            return ''
        file_object = open(self.configFileName, 'r')
        try:
             fileText = file_object.read()
        finally:
             file_object.close()
        return fileText

    def SaveConfig(self,text):
        file_object = open(self.configFileName, 'w')
        try:
             file_object.write(text)
        finally:
             file_object.close()
             

if __name__ == '__main__':

    winObj = Widget()
    winObj.mainloop()
