# ~*~ coding: utf-8 ~*~
"""
@Author: 陈乐
@Ide: Pycharm
@Time:
@Note:
@Project:
"""
from tkinter import *
import os
import load


class SmallPageUi(Toplevel):
    def __init__(self):
        super().__init__()
        self.title('移动到')
        self.geometry('500x300+250+250')
        self.resizable(width=False, height=False)

        self.home_path = ''
        self.now_path = self.home_path

        self.dir_image = PhotoImage(
            file=os.path.dirname(os.getcwd()) + os.sep + 'image' + os.sep + 'dir.png')

        # self.frame1 = Frame(self)
        # self.frame1.pack()
        self.canvas1 = Canvas(self)
        self.frame1 = Frame(self.canvas1)
        self.canvas1.pack(fill='both')
        self.canvas1.create_window((0, 0), window=self.frame1)
        self.frame1.pack(fill='both')

        self.canvas2 = None
        self.helpFiled()
        self.selectPathField(self.home_path)

    def createNewCanvas2(self):
        self.canvas2 = Canvas(self)
        self.frame2 = Frame(self.canvas2)
        self.canvas2.pack(fill='both')
        self.canvas2.create_window((0, 0), window=self.frame2)
        self.frame2.pack(fill='both')


    def getPath(self):
        return self.now_path

    # 功能键
    def helpFiled(self):
        Button(self.frame1,
               text='home',
               anchor=W,
               command=lambda: self.selectPathField(self.home_path)
               ).grid(row=0, column=0, columnspan=4, sticky=N + E + S + W)
        Button(self.frame1,
                 text='front',
                 anchor=W,
                 command=lambda: self.selectPathField(self.now_path[ : self.now_path.rfind('/')])
               ).grid(row=0, column=4, columnspan=4, sticky=N + E + S + W)

        Button(self.frame1,
                 text='OK',
                 anchor=W,
                 command=lambda: self.closeWindow()
                ).grid(row=0, column=8, columnspan=4, sticky=N + E + S + W)

        self.path_label = Label(self.frame1,
                            text=self.now_path,
                            bg='white',
                            anchor=NW,
                            font=('Arial', 12),
                            width=50, height=1)
        self.path_label.grid(row=0, column=12, columnspan=10)

    # 文件选择域
    def selectPathField(self, path):
        self.now_path = path
        self.path_label["text"] = path
        if self.canvas2 != None:
            self.canvas2.destroy()
        self.createNewCanvas2()

        files_load = load.Load()
        files_list = files_load.getFilesList(path)

        index = 1
        for item in files_list:
            if item['$t'] == 'D':
                self.showDirLine(index, item['$f'])
                index += 1


    def showDirLine(self, index, dir_name):
        # 文件夹标识
        Label(self.frame2,
              image=self.dir_image
              ).grid(row=index, column=1)
        # 文件夹打开按钮
        dir_open_button = Button(self.frame2,
                                 text=dir_name,
                                 anchor=W,
                                 command=lambda: self.selectPathField(self.now_path + '/' + dir_name))
        # 布局
        dir_open_button.grid(row=index, column=2, columnspan=8, sticky=N + E + S + W)


    def closeWindow(self):
        print(self.now_path)
        self.destroy()