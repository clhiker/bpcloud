from tkinter import *

class CoverPage(Toplevel):
    def __init__(self, remote_name):
        super().__init__()
        self.title('通知栏')
        self.geometry("400x70+200+200")
        self.is_cover = False
        self.coverEnsure(remote_name)

    def coverEnsure(self,remote_name):
        Label(self,
              text='发现'+ remote_name + '有重复，是否覆盖？',
              # anchor= W,
              font=('Time New Roman', 10),
              width=50,
              ).grid(row=0, column=0, columnspan=10, sticky=N + E + S + W)
        Button(self,
               text="确定覆盖",
               width=10,
               command=lambda: self.isCover()
               ).grid(row=1, column=2, columnspan=2, sticky=N + E + S + W)

        Button(self,
               text="取消操作",
               width=10,
               command=lambda: self.cancelCover()
               ).grid(row=1, column=6, columnspan=2, sticky=N + E + S + W)

    
    def isCover(self):
        self.is_cover = True
        self.destroy()

    def cancelCover(self):
        self.is_cover = False
        self.destroy()

    def getIsCover(self):
        return self.is_cover
