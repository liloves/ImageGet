#-*- coding: UTF-8 -*-

'''
Author: Li Geng
Meaning: App, Image get
Description: Use various module to complete the Web Detect with UI form
             if you know the http website, type it into dialog for customing to
             set the website address and smell the files in HTML
'''

# python 2.7 libirary
import os
from Tkinter import *
import tkFileDialog
import threading

# user maked
from ListTable import *
from Notebook import *
from Htmlanalyze import *
from ImageExplorer import *

# Main Widget class for showing the UI
class Widget():
    
    def __init__(self):

        # root/top widget
        self.root = Tk()   # main object of widget
        self.root.title("Get Image Serve")
        self.root.columnconfigure(0, weight=1)
        w, h = self.root.maxsize()
        self.root.geometry("{}x{}".format(w, h)) #看好了，中间的是小写字母x
        
        # menu
        self.menuInit()
        
        # switch tag frame
        nb = Notebook(self.root)
        frame1 = self.Frame1_init(nb())
        self.threadList = ListTable(nb(),3,title = 1) # List to show threading
        self.imexp = ImageExplorer(nb())  # image explorer module

        nb.add_screen(frame1, "主页")
        nb.add_screen(self.threadList(), "注册线程")
        nb.add_screen(self.imexp(), "图片浏览器")
     
        # configure variable
        self.configVar = {}
        self.configVar['parserDirect'] = 0  # 爬虫解析方向：0,向上;1,向下
        self.configVar['webAddr'] = ''
        self.rootPath = './GraphFile'    # 默认保存位置
        self.iniFile = 'store_html.xml'  # 默认参数保存文件
        self.nonFlag = 0            # 配置标记：1,空配置;0,有配置
        self.HtmlAnaObj = Htmlanalyze()

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
    
    def Frame1_init(self,root):
        # Bottom Frame element
        self.bottomForm = Frame(root)

        # active elements
        self.txt1= Text(self.bottomForm)
        self.txt1.bind("<KeyPress>", lambda e : "break")

        self.ety1 = Entry(self.bottomForm)
        self.btn2 = Button(self.bottomForm,text = "下载",command = self.btn2Clicked)
        self.btn1 = Button(self.bottomForm,text = " 确认地址",command = self.btn1Clicked)

        # grid configure
        self.txt1.grid(row=0, column=0,columnspan = 3,sticky=N+S+E+W)
        self.ety1.grid(row=1, column=0,sticky=N+S+E+W)
        self.btn1.grid(row=1, column=1,sticky=N+S+E+W)
        self.btn2.grid(row=1, column=2,sticky=N+S+E+W)

        return self.bottomForm
                       
    def Frame2_init(self,root):
        
        self.threadFrame = Frame(root)
        
        # OptionMenu
        #self.selectMenu1 = OptionMenu(self.threadFrame,'爬虫方向','上','下')
        #self.selectMenu1.grid(row=2,column = 1,sticky=N+S+E+W)

        # List
        #self.threadList = Listbox(self.threadFrame)

        # grid
        self.threadList.grid(row = 0, column = 1,rowspan = 3,stick = N+S+E+W)

        return self.threadFrame
    
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
        thisThread = threading.Thread(target=getImg,args=(htmlText, IOobj, self.rootPath, self.threadList))
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
            self.addMessage('未设置目录\n')

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

    # 保存字典至xml,使用单层字典，使用元素树结构
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


# use as start up or test
if __name__ == '__main__':

    winObj = Widget()
    winObj.mainloop()
