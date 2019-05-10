from tkinter import *

class Logout(Toplevel):
    def __init__(self):
        super().__init__()
        self.title('通知栏')
        self.geometry("300x70+200+200")
        self.logout = False
        self.logoutEnsure()
        pass
    def logoutEnsure(self,):
        Label(self,
              text='确定要注销？',
              # anchor= W,
              font=('Time New Roman', 15),
              width=30,
              ).grid(row=0, column=0, columnspan=10, sticky=N + E + S + W)
        Button(self,
               text="确定",
               width=10,
               command=lambda: self.isLogout()
               ).grid(row=1, column=2, columnspan=2, sticky=N + E + S + W)

        Button(self,
               text="取消",
               width=10,
               command=lambda: self.cancelLogout()
               ).grid(row=1, column=6, columnspan=2, sticky=N + E + S + W)


    def isLogout(self):
        self.logout = True
        self.destroy()

    def cancelLogout(self):
        self.logout = False
        self.destroy()

    def getLogout(self):
        return self.logout