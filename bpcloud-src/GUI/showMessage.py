from tkinter import *

class ShowMessage():
    def __init__(self):
        self.root = Tk()
        self.root.title('通知栏')
        self.root.geometry("300x70+200+200")
        self.logout = False

    def beginWindow(self, str):
        Label(self.root,
              text='开始' + str + '~\(≧▽≦)/~啦啦啦',
              # anchor= W,
              width=50,
              ).pack()
        Button(self.root,
               text="我知道了",
               command=self.closeWindow).pack()
        self.root.mainloop()

    def finishWindow(self, str):
        Label(self.root,
              text=str + '成功~\(≧▽≦)/~啦啦啦',
              # anchor= W,
              width=50,
              ).pack()
        Button(self.root,
               text="我知道了",
               command=self.closeWindow).pack()
        self.root.mainloop()

    def conflict(self, error):
        Label(self.root,
              text=error,
              # anchor= W,
              width=50,
              ).pack()
        Button(self.root,
               text="我知道了",
               command=self.closeWindow).pack()
        self.root.mainloop()


    def closeWindow(self):
        self.root.destroy()
