#-*- coding: UTF-8 -*-

# 引用自网络，写法采用类派生
from PIL import ImageTk,Image
import Tkinter as tk
import os
import tkFileDialog

class ImageExplorer(object):   #定义GUI的应用程序类，派生于Frmae  
    def __init__(self, master=None, filepath = None):   #构造函数，master为父窗口

        self.mainFrame = tk.Frame(master)
        #Frame.__init__(self,master)    #调用父类的构造函数
        self.createWidget()  #类成员函数，创建子组件
        #self.fresh_show()
        self.suffixArray = ['jpg','jpeg','png']  # 图像后缀名过滤
    
    def __call__(self):
        return self.mainFrame

    def createWidget(self):

        self.btnFrame=tk.Frame(self.mainFrame)   #创建窗口框架  
        self.btnFrame.grid(row = 0,column = 0,sticky = 'nsew')
        self.btnPrev=tk.Button(self.btnFrame,text="上一张",command=self.prev)  #创建按钮  
        self.btnPrev.grid(row = 0, column = 0,sticky = tk.W)
        self.btnNext=tk.Button(self.btnFrame,text="下一张",command=self.next)  #创建按钮  
        self.btnNext.grid(row = 0, column = 1,sticky = tk.W)
        self.btnAsk=tk.Button(self.btnFrame,text="打开文件夹",command=self.open_file)  #创建按钮  
        self.btnAsk.grid(row = 0, column = 2,sticky = tk.W)

        self.lblImage=tk.Label(self.mainFrame)  #创建Label组件以显示图像
        self.lblImage.grid(row = 1,column = 1, sticky = 'nsew')   #调整显示位置和大小
        self.Lst = tk.Listbox(self.mainFrame)   #创建左侧文件夹清单
        self.Lst.grid(row = 1,column = 0, sticky = 'nsew')
     
    def open_file(self,filepath = None):
        if filepath == None:
            self.filepath =  \
            tkFileDialog.askdirectory(parent=self.mainFrame,initialdir="/",  \
            title='选取保存内容的文件夹')
            #print self.filepath  # 显示打开的路径
        else:
            self.filepath = filepath

        files = os.listdir(self.filepath)   #获取图像文件名列表
        imageFiles = []
        dirArray = []
        for fileName in files:
            fileSuffix = os.path.splitext(fileName)[1][1:]
            for suffixCandidate in self.suffixArray:
                if fileSuffix == suffixCandidate:
                    imageFiles.append(fileName)
                    break

            if os.path.isdir( (self.filepath + u'\\' + fileName) ):
                dirArray.append(fileName)
        
        print dirArray
        for dir in dirArray:
            self.Lst.insert(tk.END,dir)

        self.files = imageFiles

        self.index=0    #图片索引，初始显示第一张
        self.fresh_show()
        

    def fresh_show(self):
        self.showfile()

    def prev(self):  #事件处理函数
        self.showfile(-1)
        
    def next(self):   #事件处理函数  
        self.showfile(1)
        
    def showfile(self,n = 0):  
        if len(self.files) == 0:
            return None
        self.index += n
        if self.index<0:  
            self.index=len(self.files)-1    #循环显示最后一张  
        if self.index>len(self.files)-1:  
            self.index=0    #循环显示第一张

        filename = self.filepath + '\\'+ self.files[self.index]
        imrd = Image.open(filename)
        im = self.resize_by_height(imrd,self.lblImage.winfo_screenheight())
        self.image_Tk_obj = ImageTk.PhotoImage(im)
        self.lblImage['image']= self.image_Tk_obj
        return self.image_Tk_obj
   
    def resize_by_height(self, im, con_height = 700):  
        """按照宽度进行所需比例缩放"""
        con_height = float(con_height)
        (x, y) = im.size
        w_divide_h = y/con_height
        #print w_divide_h
                     
        #print (x,y)
        x_s = int(x/w_divide_h)
        y_s = int(y/w_divide_h)
        #print (x_s, y_s)
        out = im.resize((x_s, y_s), Image.ANTIALIAS)
        return out
          


if __name__ == "__main__":
    tk1 = tk.Tk()
    path = u'E:\Code\GraphFile\[回收]满诱大胸娇妹妹【10P】 - 校园春色'
    obj = ImageExplorer(tk1,path)
    obj.mainFrame.pack()
    tk1.mainloop()

