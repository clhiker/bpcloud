# ~*~ coding: utf-8 ~*~
"""
@Author: 陈乐
@Ide: Pycharm
@Time:
@Note:
@Project:
"""
from tkinter import *


class RenameUi(Toplevel):
    def __init__(self, title, entry_text = '新建文件夹'):
        super().__init__()
        self.title(title)
        self.geometry('300x60+250+250')
        self.resizable(width=False, height=False)
        self.entry_text = entry_text
        self.file = ''
        self.selectFileField()

    def getName(self):
        return self.file

    # 文件选择域
    def selectFileField(self):
        Label(self, text="新名称:").grid(row=0, column=0)

        string_var = StringVar()

        self.new_name_entry = Entry(self, width=50, textvariable = string_var)
        string_var.set(self.entry_text) # 设置初始值
        self.new_name_entry.grid(row=0, column=1, columnspan=4, sticky=N + E + S + W)
        self.new_name_entry.bind("<Return>", self.closeWindow)
        # 获取光标焦点
        self.new_name_entry.focus_set()
        # 设置光标位置
        self.new_name_entry.icursor(5)
        Button(self, text="OK", command=self.closeWindow).grid(row=1, column=1)

    def closeWindow(self,ev = None):
        self.file = self.new_name_entry.get()
        self.destroy()
