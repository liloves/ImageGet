#-*- coding: UTF-8 -*-

from HTMLParser import HTMLParser
from cStringIO import StringIO
from urlparse import urljoin, urlparse
import zlib
import re
import os
import urllib

import re

class Htmlanalyze:

    def __init__(self):
        #self.a = [r'<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />',       \
        #     r'<meta http-equiv=Content-Type content="text/html;charset=gb2312">',           \
        #     r'<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">',    \
        #     r'<meta http-equiv="Content-Type" content="text/html; charset=gb2312" />',      \
        #     r'<meta http-equiv="content-type" content="text/html; charset=utf-8" />',       \
        #     r'<meta http-equiv="Content-Type" content="text/html; charset=gb2312" />',      \
        #     r'<meta http-equiv="Content-Type" content="text/html; charset=gb2312" />'       \
        #     ]

        self.b = r'<meta[ 	]+http-equiv=["\']?content-type["\']?[ 	]+content=["\']?text/html;[ 	]*charset=([0-9-a-zA-Z]+)["\']?'
        self.B = re.compile(self.b, re.IGNORECASE)

    def searchCharset(self, a):
        for ax in a:
            self.r1 = self.B.search(ax)
            if r1:
                print self.r1.group()
                print self.r1.group(1), len(self.r1.group())
                return self.r1.group()
            else:
                print 'not match'
                return None


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
            print fp.headers
            return zlib.decompress(bytesText, 16+zlib.MAX_WBITS)
        else:
            return bytesText
    elif fp.getcode() == 404:
        print '网址未找到'
        return ''

def getImg(html, IOobj, rootPath, Listobj, strCoder = 'gb2312'):
    imglist = regFind(r'<img.*?src="(.+?\.jpg)".*?>',html)   #解析图像列表
    titlelist = regFind(r'<head>[\s\S]*<title>([\s\S]*)</title>[\s\S]*</head>',html)

    print strCoder
    htmlTitle = titlelist[0].decode(strCoder)       #从list中提取出title的字符串变量,并解码为unicode
    htmlTitleUTF8 = htmlTitle.encode('utf-8')
    dict = [htmlTitleUTF8,str(len(imglist)),0]
    Listobj.AddRow(dict)
    IOobj.addMessage(htmlTitleUTF8 + '>>>' + '共有' + str(len(imglist)) + '张图片\n')

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




