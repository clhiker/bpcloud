from tkinter import *


class DeletePage(Toplevel):
    def __init__(self):
        super().__init__()
        self.title('通知栏')
        self.geometry("400x70+200+200")
        self.is_delete = False
        self.deleteEnsure()


    def deleteEnsure(self):
        Label(self,
              text='确定删除？',
              # anchor= W,
              font=('Time New Roman', 10),
              width=50,
              ).grid(row=0, column=0, columnspan=10, sticky=N + E + S + W)
        Button(self,
               text="确定",
               width=10,
               command=lambda: self.isDelete()
               ).grid(row=1, column=2, columnspan=2, sticky=N + E + S + W)

        Button(self,
               text="取消",
               width=10,
               command=lambda: self.cancelDelete()
               ).grid(row=1, column=6, columnspan=2, sticky=N + E + S + W)

    def isDelete(self):
        self.is_delete = True
        self.destroy()

    def cancelDelete(self):
        self.is_delete = False
        self.destroy()

    def getIsDelete(self):
        return self.is_delete