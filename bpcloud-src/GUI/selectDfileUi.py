# ~*~ coding: utf-8 ~*~
"""
@Author: 陈乐
@Ide: Pycharm
@Time:
@Note:
@Project:
"""
from tkinter import *
from tkinter.filedialog import askdirectory
from tkinter.filedialog import askopenfilename


class SelectFile(Toplevel):
    def __init__(self):
        super().__init__()
        self.title('选择文件')
        self.geometry('500x70+50+50')
        self.resizable(width=False, height=False)
        self.selectFileField()
        self.file = ''

    def getFile(self):
        return self.file

    # 文件选择域
    def selectFileField(self):
        Label(self, text="目标路径:").grid(row=0, column=0)

        self.file_entry = Entry(self, width=50)
        self.file_entry.grid(row=0, column=1, columnspan=3, sticky=N + E + S + W)

        Button(self, text="OK", command=self.closeWindow).grid(row=1, column=2)
        Button(self, text="文件选择", command=self.selectFile).grid(row=0, column=4)

    def closeWindow(self):
        self.file = self.file_entry.get()
        self.destroy()

    def selectFile(self):
        file = askopenfilename()
        self.file_entry.delete(0, END)
        self.file_entry.insert(0, file)        


class SelectDir(Toplevel):
    def __init__(self):
        super().__init__()
        self.title('选择文件夹')
        self.geometry('500x70+50+50')  # 窗口大小
        self.resizable(width=False, height=False)
        self.selectPathField()
        self.dir = ''

    # 文件选择域
    def selectPathField(self):

        Label(self, text="目标路径:").grid(row=0, column=0)
        self.dir_entry = Entry(self, width=50)
        self.dir_entry.grid(row=0, column=1, columnspan=3, sticky=N+E+S+W)
        Button(self, text="OK", command=self.closeWindow).grid(row=1, column=2)
        Button(self, text="选择文件夹", command=self.selectPath).grid(row=0, column=4)


    # 关闭标签页
    def closeWindow(self):
        self.dir = self.dir_entry.get()
        self.destroy()

    # 打开当地文件对话框
    def selectPath(self):
        path = askdirectory()
        try:
            self.dir_entry.delete(0,END)
            self.dir_entry.insert(0, path)
        except :
            pass

    def getDir(self):
        return self.dir
