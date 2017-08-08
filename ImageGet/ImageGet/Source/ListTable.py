#-*- coding: UTF-8 -*-
from Tkinter import *

class ListTable(object):
    """has multiple columns of ListBox"""

    def __init__(self, root, columns = 3, **args):
        self.ListFrame = Frame(root)
        self.Table = []
        self.columns = columns

        for key,value in args.items():
            if key == 'listname':
                pass

        for i in range(0, columns):
            ListboxObj = Listbox(self.ListFrame)
            self.Table.append(ListboxObj)
            ListboxObj.grid(row = 0, column = i, sticky=N+S+E+W)
            ListboxObj.bind("<<ListboxSelect>>",self.ListSelectChange)


    
    def __call__(self):
        return self.ListFrame    # 返回显示框架的引用对象

    def ListFresh(self,ListObj, ListItems):
        for items in ListItems:
            ListObj.insert(END,items)

    def ListSelectChange(self,index):
        print index

    def AddRow(self,dict):
        for i in range(0,self.columns):
            self.Table[i].insert(END,dict[i])
     