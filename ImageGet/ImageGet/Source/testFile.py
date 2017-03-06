#-*- coding: UTF-8 -*-
from ImageGet import *
import urllib2
import urllib

##from sgmllib import SGMLParser
## 
##class ListName(SGMLParser):
##	def __init__(self):
##		SGMLParser.__init__(self)
##		self.is_h4 = ""
##		self.name = []
##	def start_h4(self, attrs):
##		self.is_h4 = 1
##	def end_h4(self):
##		self.is_h4 = ""
##	def handle_data(self, text):
##		if self.is_h4 == 1:
##			self.name.append(text)
##
##content = urllib2.urlopen('http://list.taobao.com/browse/cat-0.htm').read()
##listname = ListName()
##listname.feed(content)




webAddr = 'http://www.gamersky.com/'
iparser = AnchorParser()
print iparser.getLink(webAddr)


reg = r'<meta.+?charset\"?=(.+?)\"?.+?>'
print regFind(reg,getHtml(webAddr))

    
