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
        # widget main
        self.root = Tk()
        #self.root.minsize(300, 200)
        self.root.title("Get Image Serve")

        # menu
        self.menuInit()

        # active elements
        self.txt1= Text(self.root)
        #self.txt1.bind("<KeyPress>", lambda e : "break")

        # Bottom Frame element
        self.bottomForm = Frame()
        self.ety1 = Entry(self.bottomForm,width = 40)
        self.btn2 = Button(self.bottomForm,width = 10,text = "下载",command = self.btn2Clicked)
        self.btn1 = Button(self.bottomForm,width = 10,text = " 确认地址",command = self.btn1Clicked)
        self.ety1.grid(row=0, column=0)
        self.btn1.grid(row=0, column=1)
        self.btn2.grid(row=0, column=2)

        ## main pack
        self.txt1.grid(row=0, column=0)
        self.bottomForm.grid(row=2, column=0, sticky=W)

        # configure variable
        self.configVar = {}
        self.configVar['parserDirect'] = 0  # 爬虫解析方向：0,向上;1,向下
        self.configVar['webAddr'] = ''
        self.rootPath = './GraphFile'    # 默认保存位置
        self.iniFile = 'store_html.xml'  # 默认参数保存文件
        self.nonFlag = 0            # 配置标记：1,空配置;0,有配置

        # work variable
        self.threadpool = []        # 线程池

        # startup message
        self.addMessage('请先到菜单（参数设置）->（设置存储文件夹）设置一个存档文件夹\n')
        self.addMessage('退出前到菜单（参数设置）->（保存当前配置）保存当前进度\n')

        
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
        filemenu.add_command(label = "打开存储文件夹", command = self.openRoot)
        filemenu.add_separator()
        filemenu.add_command(label = "重新加载配置文件", command = self.loadConfig)
        filemenu.add_command(label = "保存当前配置", command = self.btn3Clicked)
        filemenu.add_separator()  
        filemenu.add_command(label = "设置爬虫方向",command = self.changeDirect) 
        filemenu.add_separator()
        filemenu.add_command(label = "设置数据库存储", command = self.btn3Clicked)
        
        menubar.add_cascade(label = "参数配置", menu = filemenu)

        # child menu
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label = "检查运行线程", command = self.checkThread)
        

        menubar.add_cascade(label = "查看运行状态", menu = filemenu)
        
        # link
        self.root.config(menu=menubar)

    def showWebAddr(self):
        if self.configVar['webAddr'] == '':
            self.addMessage('目标地址为空\n')
        else:
            self.addMessage('设置地址为'+ self.configVar['webAddr'] + '\n')
    
    def btn1Clicked(self):
        if self.ety1.get() != '':
            self.configVar['webAddr'] = self.ety1.get()
            self.addMessage('设置地址为:'+self.configVar['webAddr'] + '\n')
        else:
            self.addMessage('设置地址为空\n')
    
    def btn2Clicked(self):
        if self.configVar['webAddr'] == '' :
            self.addMessage('目前没有读到上次结束的地址,请输入一个网址\n')
        else:
            try:
                thisThread = threading.Thread(target=self.webDetect,args=(self.configVar['webAddr'],self))
                thisThread.start()
            except Exception,e:
                print '线程创建或启动异常:',Exception,':',e
    
    # 保存当前状态
    def btn3Clicked(self):
        self.addMessage('保存地址为:'+self.configVar['webAddr'] + '\n')
        cfgObj = Config(self.rootPath + '/'+ self.iniFile)
        cfgObj.XmlSave(self.configVar)
    
    def mainloop(self):
        self.root.mainloop()

    # 启动网页分析
    def webDetect(self,webAddr,IOobj):
        IOobj.addMessage('准备打开地址:' + webAddr + '\n')
        htmlText = getHtml(webAddr)
        thisThread = threading.Thread(target=getImg,args=(htmlText, IOobj, self.rootPath))
        thisThread.start()
        self.rptl(htmlText, webAddr)

    # 爬虫分析函数
    # reptile analyze
    def rptl(self, htmlText,webAddr):
        smellWord = r'<a href=(.+?\.html)>.*?</a>'
        GraspList = regFind(smellWord, htmlText)
        # 定制爬虫方式
        try:
            self.configVar['webAddr'] =  'http://' + urlparse(webAddr).netloc + GraspList[int(self.configVar['parserDirect'])]    #爬虫目标地址
        except Exception,e:
            print '爬虫问题',Exception,':',e
        return GraspList        
            
    # 改变爬虫方向
    def changeDirect(self):
        if self.configVar['parserDirect'] == '1':
            self.configVar['parserDirect'] = '0'
        elif self.configVar['parserDirect'] == '0':
            self.configVar['parserDirect'] = '1'
        self.addMessage('爬虫设置方向为'+str(self.configVar['parserDirect'])+'\n')
    
    # 文本消息窗
    def addMessage(self, text, position = END):
        self.txt1.insert(position, text)

    # 加载配置文件
    def loadConfig(self):
        # 读取历史配置
        FilePath = self.rootPath + '/'+ self.iniFile
        if os.path.exists(FilePath):
            self.ConfigObj = Config(FilePath)         #配置文件
            elmtdic = self.ConfigObj.XmlLoad()  #加载保存的地址
            for key,val in elmtdic.iteritems():
                if self.configVar.has_key(key):
                    self.configVar[key] = val
            if self.configVar['webAddr'] == '':
                self.nonFlag = 1
                self.addMessage('目前没有读到上次结束的地址,请输入一个网址\n')
            else:
                self.addMessage('上次结束的地址为:' + self.configVar['webAddr'] + '\n')
        else:
            self.addMessage('没有发现配置文件\n')

    def directoryConfig(self):
        getPath =  \
            tkFileDialog.askdirectory(parent=self.root,initialdir="/",  \
            title='选取保存内容的文件夹')
        if getPath != '':
            self.addMessage(u'设置目录为: ' + getPath + u'\n')
            self.rootPath = getPath
            self.loadConfig()
        else:
            self.addMessage(u'未设置目录\n')

    def openRoot(self):
        os.startfile(self.rootPath)

    def checkThread(self):
        couts = threading.active_count()
        self.addMessage('当前运行线程数:'+str(couts)+'\n')

            

# configuration file save & load
class Config():
    def __init__(self,configFileName = '.\store_html.xml'):
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

    # 保存字典至xml,使用单层字典，后续可能会加入多级树结构
    def XmlSave(self,dic):
        from xml.etree.ElementTree import Element,SubElement,tostring
        from xml.dom.minidom import parseString
        info = Element('elements')
        for key,val in dic.iteritems():
            SubElement(info,key).text = str(val)
        dom = parseString(tostring(info))
        filename = self.configFileName
        f = open(filename, "w")
        f.write(dom.toprettyxml('    '))
        f.close()
    
    # 加载xml至字典
    def XmlLoad(self):
        from xml.etree import ElementTree
        filename = self.configFileName
        dic = {}
        tree = ElementTree.parse(filename)
        for elmt in tree.getiterator():
            dic[elmt.tag] = elmt.text
        return dic


if __name__ == '__main__':

    winObj = Widget()
    winObj.mainloop()
