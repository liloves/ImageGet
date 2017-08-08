#-*- coding: UTF-8 -*-

from Tkinter import *

class Notebook(object):

    def __init__(self, master):
        # 所有内容附于master框架，可能是Frame也可能是Tk主界面
        # 使用grid而不是pack放置对象
        self.active_fr = None
        self.count = 0
        self.choice = IntVar(0)
        ''' 
        暂不使用pack函数的对齐
        side=LEFT
        if side in (TOP, BOTTOM):
            self.side = LEFT
        else:
            self.side = TOP
        '''
        
        self.rb_fr = Frame(master, borderwidth=0, relief=RIDGE)  # 标签栏的框架
        self.rb_fr.grid(row = 0, column = 0, stick = N+S+E+W)
        self.screen_fr = Frame(master, borderwidth=0, relief=RIDGE)   # 内容显示页的框架
        self.screen_fr.grid(row = 1, column = 0, stick = N+S+E+W)

    def __call__(self):
        return self.screen_fr    # 返回显示框架的引用对象

    def add_screen(self, fr, title):
        b = Radiobutton(self.rb_fr, text=title, indicatoron=0, variable=self.choice, value=self.count, 
                        command=lambda:self.display(fr))
        b.grid(row = 0, column = self.count,stick = W)
        if not self.active_fr:
            fr.grid(row = 1, column = 0, stick = N+S+E+W)
            self.active_fr = fr
        self.count += 1

    def display(self, fr):
        self.active_fr.grid_forget()   # 使用grid的消隐函数
        fr.grid(row = 1, column = 0)   # 统一放在第2行
        self.active_fr = fr            # 记录当前切换的框架


# 范例
if __name__ == "__main__":
    root = Tk()
    nb = Notebook(root, LEFT)

    """
    生成不同的框架（面板），每个都把NB当做"master"
    """
    f1 = Frame(nb())
    b1 = Button(f1, text = "Button 1")
    e1 = Entry(f1)

    b1.pack(fill=BOTH, expand=1)
    e1.pack(fill=BOTH, expand=1)

    f2 = Frame(nb())
    b2 = Button(f2, text = "Button 2")
    b3 = Button(f2, text = "Beep 2", command = Tk.bell)
    b2.pack(fill=BOTH, expand=1)
    b3.pack(fill=BOTH, expand=1)
    f3 = Frame(nb())

    nb.add_screen(f1, "Screen 1")
    nb.add_screen(f2, "Screen 2")
    nb.add_screen(f3, "dummy")
    root.mainloop()
