'''
版本1.3
添加了文件下载能力
添加了上传下载的暂停取消功能
图标的小幅度修改
'''

from tkinter import *
import time
import os
import threading
import selectDfileUi
import load
import renameWindow
import movePage
import configparser
import logout
import showMessage
import coverPage
import deletePage

class DriverUi(object):
    # 构造函数
    def __init__(self):
        self.root = Tk()
        self.root.configure(background='palevioletred')    #可以在这里设置等候
        # self.root.configure(image='../image/loading.gif')
        self.page_record = []
        self.root_path = ''
        #
        self.select_list = []
        self.remote_filesname_list = []
        self.isSelectAll = False
        self.frame1_3 = None
        # # 上传队列
        self.upload_queue = []
        # self.upload_frame_list = []
        # # 等待上传队列
        self.wait_upload_queue = []
        # self.wait_upload_frame_list = []
        # # 下载队列
        self.download_queue = {}
        # self.download_frame_list = []
        # # 等待下载队列
        self.wait_download_queue = {}
        # self.wait_download_frame_list = []
        #
        self.finish_download_queue = []
        self.downloading_thread = {}

        self.dfiles_num = 0
        self.home_text = '我的网盘:'
        self.path_label = None

        self.dir_menubar = Menu(self.frame1_3, tearoff=False)  # 创建一个菜单
        self.file_menubar = Menu(self.frame1_3, tearoff=False)  # 创建一个菜单
        #
        self.now_path = self.root_path
        self.getImage()
        self.user_label = None
        #
        config = configparser.ConfigParser()
        config.read('local.ini')
        self.MAX_LOAD = int(config.get('config', 'max_load_number'))

        HomeDir = os.path.expanduser('~')
        ConfigDir = HomeDir + os.sep + '.bypy'
        TokenFileName = 'bypy.json'
        self.token_file_path = ConfigDir + os.sep + TokenFileName

    def closeMeun(self):
        self.file_menubar.delete(0,END)
        self.dir_menubar.delete(0, END)


    def getImage(self):
        self.dir_image = PhotoImage(
            file=os.path.dirname(os.getcwd()) + os.sep + 'image' + os.sep + 'dir.png')
        self.file_image = PhotoImage(
            file=os.path.dirname(os.getcwd()) + os.sep + 'image' + os.sep + 'file.png')
        self.home_image = PhotoImage(
            file=os.path.dirname(os.getcwd()) + os.sep + 'image' + os.sep + 'home.png')
        self.new_folder_image = PhotoImage(
            file=os.path.dirname(os.getcwd()) + os.sep + 'image' + os.sep + 'new-folder.png')
        # self.sort_image = PhotoImage(
        #     file=os.path.dirname(os.getcwd()) + os.sep + 'image' + os.sep + 'sort.png')
        self.flush_image = PhotoImage(
            file=os.path.dirname(os.getcwd()) + os.sep + 'image' + os.sep + 'flush.png')
        self.choose_image = PhotoImage(
            file=os.path.dirname(os.getcwd()) + os.sep + 'image' + os.sep + 'choose.png')
        self.choosed_image = PhotoImage(
            file=os.path.dirname(os.getcwd()) + os.sep + 'image' + os.sep + 'chose.png')
        self.front_image = PhotoImage(
            file=os.path.dirname(os.getcwd()) + os.sep + 'image' + os.sep + 'front.png')

    # 初始化窗口
    def setWindow(self):
        self.root.title('百度网盘Python客户端')
        self.root.geometry('700x500+200+200')
        self.root.resizable(False, False)

        # 1、4个功能键区域
        self.canvas1 = Canvas(self.root)
        self.frame1 = Frame(self.canvas1)
        self.canvas1.pack(fill='both')
        self.canvas1.create_window((0, 0), window=self.frame1)
        self.frame1.pack(fill='both')
        self.userLogInfo()


    # 功能选择按钮
    def userLogInfo(self):
        self.user_label = Label(
            self.frame1, text='请先登录', width=55,
            font=('Arial', 15),
        )
        self.user_label.grid(row=0, column=0, columnspan=15, sticky=N + E + S + W)


    # 第1个，文件列表页面
    def showFileListPage(self):
        # 首先检查之前页面的信息，并删除之前的页面
        if len(self.page_record) != 0:
            for item in self.page_record[0]:
                item.destroy()
            for item in self.page_record[1]:
                item.destroy()
            del self.page_record[0]
            del self.page_record[0]

        # 1、页面功能键
        self.canvas1_1 = Canvas(self.root)
        self.frame1_1 = Frame(self.canvas1_1)
        self.canvas1_1.pack(fill='both')
        self.canvas1_1.create_window((0, 0), window=self.frame1_1)
        self.frame1_1.pack(fill='both')
        self.keyOfFileList()

        # 2、文件信息展示栏
        self.canvas1_2 = Canvas(self.root)
        self.frame1_2 = Frame(self.canvas1_2)
        self.canvas1_2.pack(fill='both')
        self.canvas1_2.create_window((0, 0), window=self.frame1_2)
        self.frame1_2.pack(fill='both')
        self.showFileInfo()

        self.page_record.append([self.frame1_1, self.frame1_2])
        self.page_record.append([self.canvas1_1, self.canvas1_2])

        # 3、页面信息
        self.showObjectPageInNowPath(self.now_path)

    # 展示当前文件夹下的所有项
    def showObjectPageInNowPath(self, now_path):
        self.canvas1_3 = Canvas(self.root, height=400)
        self.frame1_3 = Frame(self.canvas1_3)
        # self.frame1_3.pack(fill='both')
        self.vsb1 = Scrollbar(self.root, command=self.canvas1_3.yview)
        self.canvas1_3.configure(yscrollcommand=self.vsb1.set)
        self.vsb1.pack(side="right", fill="y")
        self.canvas1_3.pack(fill='both')
        self.canvas1_3.create_window((4, 4), window=self.frame1_3, anchor="nw",
                                     tags="self.frame")
        self.frame1_3.bind("<Configure>", self.OnFrameConfigure1_3)
        self.canvas1_3.bind('<MouseWheel>', self.onMousewheel)
        self.canvas1_3.bind('<Button-4>', self.onMousewheel)
        self.canvas1_3.bind('<Button-5>', self.onMousewheel)

        # 将当前页面记录在案
        self.page_record[0].append(self.frame1_3)
        self.page_record[1].append(self.canvas1_3)
        self.page_record[1].append(self.vsb1)

        self.showObjectListPage()

    def onMousewheel(self, event):
        self.canvas1_3.yview_scroll(-1 * round(event.delta / 120), "units")

    # 1、文件列表页面的功能键
    def keyOfFileList(self):
        self.functionalButton()
        self.showFilePathLabel()


    # 展示文件路径标签
    def showFilePathLabel(self):
        self.path_label = Label(self.frame1_1,
                            text=self.home_text,
                            bg='pink',
                            font=('Arial', 12),
                            width=70, height=1
                            )
        self.path_label.grid(row=1, column=5, columnspan=10)

    # 1、功能按钮
    def functionalButton(self):
        Button(
            self.frame1_1, image=self.front_image, font=15, command=self.returnPreviousPage
        ).grid(row=1, column=0)
        Button(
            self.frame1_1, image=self.flush_image, font=15, command=self.flush
        ).grid(row=1, column=2)
        Button(
            self.frame1_1,
            width=20,
            height=20,
            image=self.home_image, font=15, command=self.goHomePage
        ).grid(row=1, column=3)
        Button(
            self.frame1_1, image=self.new_folder_image, font=15, command=self.newFolder
        ).grid(row=1, column=4)

        # 多级菜单上传按钮
        upload_button = Menubutton(
            self.frame1_1, text='上传', font=15
        )
        upload_button.grid(row=1, column=1)
        upload_button.menu = Menu(upload_button)
        upload_button.menu.add_command(label='上传文件', command=self.uploadFileResponse)
        upload_button.menu.add_command(label='上传文件夹', command=self.uploadDirResponse)
        upload_button['menu'] = upload_button.menu


    # 2、文件信息展示栏
    def showFileInfo(self):
        # 全选按钮
        Button( self.frame1_2,
                image=self.choose_image,
                command=self.selectAll
            ).grid(row=2, column=0, sticky=N + E + S + W)
        # 文件名标识（标签）
        Label(self.frame1_2,
              text='文件名↓',
              # anchor= W,
              width=50 ,
              ).grid(row=2, column=2, padx=10, columnspan=8, sticky=N + E + S + W)
        # 文件大小展示标识
        Label(self.frame1_2,
              text='大小',
              width=20,
              ).grid(row=2, column=10, padx=10, columnspan=5, sticky=N + E + S + W)
        # 修改时间标识
        Label(self.frame1_2,
              text='修改时间↓',
              anchor=W,
              width=10,
              ).grid(row=2, column=15, padx=10, columnspan=5, sticky=N + E + S + W)

    # 3、文件页面展示
    def showObjectListPage(self):
        dir_info = []
        file_info = []
        files_load = load.Load()
        files_list = files_load.getFilesList(self.now_path)
        self.dfiles_num = len(files_list)
        for item in files_list:
            if item['$t'] == 'D':
                dir_info.append([item['$f'], item['$s']])
            elif item['$t'] == 'F':
                file_info.append([item['$f'], item['$s'], item['$c']])

            self.remote_filesname_list.append(item)

        i = 0
        # 文件文件名输出
        for item in dir_info:
            self.show_dir_line(i, item[0], item[1])
            i += 1
        for item in file_info:
            self.show_file_line(i, item[0], item[1], item[2])
            i += 1

    # 文件夹栏目一行的消息
    def show_dir_line(self, index, dir_name, modify_time):
        # 选中信号
        Button(
            self.frame1_3, image=self.choose_image, command=lambda: self.selectOne(index)
        ).grid(row=index, column=0)
        # 文件夹标识
        Label(self.frame1_3,
              image=self.dir_image,
              width=20,
              height=20,
              ).grid(row=index, column=1)
        # 文件夹打开按钮
        dir_open_button = Button(self.frame1_3,
                                 text=dir_name,
                                 width=50,
                                 anchor=W,
                                 command=lambda: self.selectOne(index)
                                 )
        # 绑定打开文件夹
        dir_open_button.bind('<Double-Button-1>',
                             self.openDirHandlerAdaptor(
                                self.openDir, relay_path=dir_name))
        # 绑定右键事件
        dir_open_button.bind("<Button-3>", lambda event: self.dirRightKeyMenu(event, index, dir_name))  # 绑定右键鼠标事件
        # 布局
        dir_open_button.grid(row=index, column=2, columnspan=8, sticky=N + E + S + W)

        # 大小标签
        Label(self.frame1_3,
              width=13,
              text='--',
              ).grid(row=index, column=10, columnspan=5)
        # 修改时间
        Label(self.frame1_3,
              width=20,
              text=modify_time,
              ).grid(row=index, column=15, columnspan=5)

    # 文件栏目一行的消息
    def show_file_line(self, index, filename, file_size, modify_time):
        # 选中信号
        Button(
            self.frame1_3, image=self.choose_image, command=lambda: self.selectOne(index)
        ).grid(row=index, column=0)

        # 文件标识
        Label(self.frame1_3,
              image=self.file_image,
              ).grid(row=index, column=1)
        # 文件选中单击按钮
        file_open_button = Button(
            self.frame1_3, text=filename, anchor=W,
            width=50,
            command=lambda: self.selectOne(index)
        )

        # 绑定右键事件
        file_open_button.bind("<Button-3>", lambda x: self.fileRightKeyMenu(x, index, filename))  # 绑定右键鼠标事件

        file_open_button.grid(row=index, column=2, columnspan=8, sticky=N + E + S + W)

        # 文件大小
        Label(self.frame1_3,
              text=self.modifySizeNameFromFile(file_size),
              anchor=W
              ).grid(row=index, column=10, columnspan=5)
        # 修改时间
        Label(self.frame1_3,
              text=modify_time,
              anchor=W
              ).grid(row=index, column=15, columnspan=5)

    # 中间适配器
    def openDirHandlerAdaptor(self, fun, **kwds):
        return lambda event, fun=fun, kwds=kwds: fun(event, **kwds)

    # 打开文件夹
    def openDir(self, event, relay_path):
        self.removeFileListPage()
        self.now_path = self.now_path + '/' + relay_path
        self.showObjectPageInNowPath(self.now_path)
        # 取消勾选
        self.isSelectAll = True
        self.selectAll()

        # 更改显示栏
        self.flushPathLable()

        self.closeMeun()

    # 每一行的单选信号
    def selectOne(self, index):
        if index in self.select_list:
            Button(
                self.frame1_3,
                image=self.choose_image,
                command=lambda: self.selectOne(index)
            ).grid(row=index, column=0)
            self.select_list.remove(index)
        else:
            Button(
                self.frame1_3,
                image=self.choosed_image,
                command=lambda: self.selectOne(index)
            ).grid(row=index, column=0)
            self.select_list.append(index)

        self.closeMeun()
    # 每一行的单选信号
    def onlySelectOne(self, index):
        if index in self.select_list:
            pass
        else:
            Button(
                self.frame1_3,
                image=self.choosed_image,
                command=lambda: self.selectOne(index)
            ).grid(row=index, column=0)
            self.select_list.append(index)

    # 全选信号
    def selectAll(self):
        # 取消全选
        if self.isSelectAll:
            # 全选按钮
            Button(
                self.frame1_2, image=self.choose_image, command=self.selectAll
            ).grid(row=2, column=0, sticky=N + E + S + W)


            self.select_list.clear()
            for i in range(self.dfiles_num):
                self.select_list.append(i)
            # 将之下的所有文件取消勾选
            for index in range(self.dfiles_num):
                self.selectOne(index)
                # if index in self.select_list:
                #     Button(
                #         self.frame1_3,
                #         image=self.choose_image,
                #         command=lambda: self.selectOne(index)
                #     ).grid(row=index, column=0)
                #     self.select_list.remove(index)
                # else:
                #     pass
            self.isSelectAll = False
        # 全选
        else:
            # 全选按钮
            Button(
                self.frame1_2, image=self.choosed_image, command=self.selectAll
            ).grid(row=2, column=0, sticky=N + E + S + W)

            # 将之下的所有文件勾选
            self.select_list.clear()
            for index in range(self.dfiles_num):
                self.selectOne(index)
            self.isSelectAll = True

        self.closeMeun()

    # 文件夹右键菜单
    def dirRightKeyMenu(self, event,index, dir_name):
        self.onlySelectOne(index)
        self.closeMeun()
        # 右键功能要有：下载，打开，删除，重命名，移动
        self.dir_menubar.add_command(label='下载', command=lambda: self.downloadResponse(event))
        self.dir_menubar.add_command(label='打开', command=lambda: self.openDir(event, dir_name))
        self.dir_menubar.add_command(label='删除', command=lambda: self.deleteResponse(event))
        self.dir_menubar.add_command(label='重命名', command=lambda: self.renameResponse(event, dir_name))
        self.dir_menubar.add_command(label='移动到', command=lambda: self.moveResponse(event))
        self.dir_menubar.add_command(label='复制到', command=lambda: self.copyResponse(event))

        self.dir_menubar.post(event.x_root, event.y_root)

    # 删除
    def deleteResponse(self, even):
        delete_page_ui = deletePage.DeletePage()
        self.root.wait_window(delete_page_ui)
        is_delete = delete_page_ui.getIsDelete()
        if is_delete:
            for index in self.select_list:
                self.beginDelete(self.remote_filesname_list[index]['$f'])
            self.flush()
        else:
            return

    def beginDelete(self, name):
        delete_dir_client = load.Load()
        remote_path = self.now_path + '/' + name
        delete_dir_client.remove(remote_path)


    # 重命名
    def renameResponse(self, event, old_name):
        rename_ui = renameWindow.RenameUi('重命名', old_name)
        self.root.wait_window(rename_ui)
        new_name = rename_ui.getName()
        if new_name == '':
            return
        # 命名冲突
        for item in self.remote_filesname_list:
            if item['$f'] == new_name:
                show_message_ui = showMessage.ShowMessage()
                show_message_ui.conflict('命名冲突了( ⊙ o ⊙ )啊！')
                return


        old_path = self.now_path + '/' + old_name
        new_path = self.now_path + '/' + new_name

        rename_client = load.Load()
        rename_client.rename(old_path, new_path)
        self.flush()

    # 移动操作
    def moveResponse(self, event):
        small_page = movePage.SmallPageUi()
        self.root.wait_window(small_page)
        new_up_path = small_page.getPath()

        if new_up_path == self.now_path:
            self.flush()

        # 同级目录检查
        for index in self.select_list:
            old_path = self.now_path + '/' + self.remote_filesname_list[index]['$f']
            # if old_path == new_up_path:
            if new_up_path.find(old_path) == 0:
                error_ui = showMessage.ShowMessage()
                error_ui.conflict('不能移动到自身或子目录下')
                return

        for index in self.select_list:
            old_path = self.now_path + '/' + self.remote_filesname_list[index]['$f']
            new_path = new_up_path + '/' + self.remote_filesname_list[index]['$f']
            self.beginMove(old_path, new_path)
        self.flush()

    def beginMove(self, old_path, new_path):
        move_client = load.Load()
        move_client.move(old_path, new_path)


    # 复制操作
    def copyResponse(self, event):
        small_page = movePage.SmallPageUi()
        self.root.wait_window(small_page)
        new_up_path = small_page.getPath()
        if new_up_path == self.now_path:
            self.flush()

        # 同级目录检查
        for index in self.select_list:
            old_path = self.now_path + '/' + self.remote_filesname_list[index]['$f']

            # if old_path == new_up_path:
            if new_up_path.find(old_path) == 0:
                error_ui = showMessage.ShowMessage()
                error_ui.conflict('不能将复制到自身或子目录下')
                return

        for index in self.select_list:
            new_path = new_up_path + '/' + self.remote_filesname_list[index]['$f']
            old_path = self.now_path + '/' + self.remote_filesname_list[index]['$f']
            self.beginCopy(old_path, new_path)

        self.flush()

    def beginCopy(self, old_path, new_path):
        move_client = load.Load()
        move_client.copy(old_path, new_path)


    # 文件右键菜单
    def fileRightKeyMenu(self, event, index, filename):
        self.onlySelectOne(index)
        self.closeMeun()
        # 右键功能要有：下载，打开，删除，重命名，移动，属性
        self.file_menubar.add_command(label='下载', command=lambda: self.downloadResponse(event))
        self.file_menubar.add_command(label='删除', command=lambda: self.deleteResponse(event))
        self.file_menubar.add_command(label='重命名', command=lambda: self.renameResponse(event, filename))
        self.file_menubar.add_command(label='移动到', command=lambda: self.moveResponse(event))
        self.file_menubar.add_command(label='复制到', command=lambda: self.copyResponse(event))

        self.file_menubar.post(event.x_root, event.y_root)


    # 下载事件
    def downloadResponse(self, event):
        # 先选择下载目的文件夹
        download_ui = selectDfileUi.SelectDir()
        self.root.wait_window(download_ui)
        save_path = download_ui.getDir()
        if save_path == '':
            return

        # 覆盖检查
        local_dfile_list = os.listdir(save_path)

        for index in self.select_list:
            remote_name = self.remote_filesname_list[index]['$f']
            remote_size = self.remote_filesname_list[index]['$s']
            if remote_name in local_dfile_list:
                cover_page_ui = coverPage.CoverPage(remote_name)
                self.root.wait_window(cover_page_ui)
                is_cover = cover_page_ui.getIsCover()
                if is_cover:
                    if self.remote_filesname_list[index]['$t'] == 'F':
                        local_path = save_path
                        remote_path = self.now_path + '/' + remote_name
                        self.beginDownloadFile(local_path, remote_path, remote_size)
                    else:
                        local_path = save_path + os.sep + remote_name
                        if not os.path.exists(local_path):
                            os.mkdir(local_path)
                        remote_path = self.now_path + '/' + remote_name
                        self.beginDownloadDir(local_path, remote_path)
                else:
                    pass
            else:
                if self.remote_filesname_list[index]['$t'] == 'F':
                    local_path = save_path
                    remote_path = self.now_path + '/' + remote_name
                    self.beginDownloadFile(local_path, remote_path, remote_size)
                else:
                    local_path = save_path + os.sep + remote_name
                    if not os.path.exists(local_path):
                        os.mkdir(local_path)
                    remote_path = self.now_path + '/' + remote_name
                    self.beginDownloadDir(local_path, remote_path)

        self.flush()

    def beginDownloadFile(self,local_path, remote_path, remote_size):
        # 记录下下载文件
        if len(self.download_queue) > self.MAX_LOAD:
            self.wait_download_queue[remote_path] = ((remote_path, remote_size, local_path))

        else:
            download_client = load.Load()
            download_client.setRemotePath(remote_path)
            download_client.setLocalPath(local_path)
            download_client.setRemoteSize(remote_size)

            t = threading.Thread(target=download_client.download, args=(
                remote_path, local_path, self.finish_download_queue))
            t.setDaemon(True)
            t.start()

            self.download_queue[remote_path] = download_client
            self.downloading_thread[remote_path] = t

    # 下载文件夹
    def beginDownloadDir(self,local_path, remote_path):
        # 首先获取目录列表
        download_client = load.Load()
        dir_list = download_client.getFilesList(remote_path)

        for item in dir_list:
            if item['$t'] == 'F':
                remote_size = item['$s']
                remote_file_path = remote_path + '/' + item['$f']
                self.beginDownloadFile(local_path, remote_file_path, remote_size)
            else:
                remote_path = remote_path + '/' + item['$f']
                local_path = local_path + os.sep + item['$f']
                if not os.path.exists(local_path):
                    os.mkdir(local_path)
                self.beginDownloadDir(remote_path, local_path)


    # < 按钮
    def returnPreviousPage(self):
        if self.now_path == self.root_path:
            return
        index = self.now_path.rfind('/')
        self.now_path = self.now_path[:index]
        self.removeFileListPage()
        self.showObjectPageInNowPath(self.now_path)

        # 更改显示栏
        self.flushPathLable()
        self.closeMeun()
        self.cancelSelectAll()


    # 上传文件夹按钮
    def uploadDirResponse(self):
        upload_ui = selectDfileUi.SelectDir()
        self.root.wait_window(upload_ui)
        local_path = upload_ui.getDir()
        if local_path == '':
            return

        local_name = local_path[local_path.rfind('/') + 1 :]

        # 覆盖检测
        if local_name in self.remote_filesname_list:
            cover_page_ui = coverPage.CoverPage(local_name['$f'])
            self.root.wait_window(cover_page_ui)
            is_cover = cover_page_ui.getIsCover()
            if is_cover:
                pass
            else:
                return

        remote_path = self.now_path + '/' + local_name
        upload_dir_client = load.Load()
        upload_dir_client.mkdir(remote_path)
        self.flush()
        t = threading.Thread(target=upload_dir_client.upload, args=(
            local_path, remote_path))
        t.setDaemon(True)
        t.start()

        self.closeMeun()

    #     recode_now_path = self.now_path
    #     dir_name = local_path[local_path.rfind('/') + 1:]
    #     # remote_path = self.now_path + os.sep + dir_name
    #
    #     self.createNewFolder(dir_name)
    #     self.uploadRecursion(local_path, dir_name, recode_now_path)
    #
    # def uploadRecursion(self, local_path, dir, recode_now_path):
    #     object_list = os.listdir(local_path)
    #     for item in object_list:
    #         local_path = local_path + os.path.sep + item
    #         dir_path = dir + os.sep + item
    #
    #         if os.path.isdir(local_path):
    #             self.createNewFolder(dir_path)
    #             self.uploadRecursion(local_path, dir_path, recode_now_path)
    #         else:
    #             # filename = item
    #             # file_path = local_path + os.sep + filename
    #             remote_path = recode_now_path + '/' + dir_path
    #             upload_client = load.Load()
    #             t = threading.Thread(target=upload_client.upload, args=(
    #                 local_path, remote_path))
    #             t.start()
    #             # 然后开始上传
    #             self.upload_queue.append([local_path, upload_client])

    # 上传文件按钮
    def uploadFileResponse(self):
        # 首先获取文件名
        upload_ui = selectDfileUi.SelectFile()
        self.root.wait_window(upload_ui)
        local_path = upload_ui.getFile()
        if local_path == '':
            return

        local_name = local_path[local_path.rfind('/') + 1 : ]

        # 覆盖检测
        if local_name in self.remote_filesname_list:
            cover_page_ui = coverPage.CoverPage(local_name['$f'])
            self.root.wait_window(cover_page_ui)
            is_cover = cover_page_ui.getIsCover()
            if is_cover:
                pass
            else:
                return

        # 开启上传线程
        upload_client = load.Load()
        t = threading.Thread(target=upload_client.upload, args=(
            local_path, self.now_path))
        t.setDaemon(True)
        t.start()
        # 加入上传队列
        self.upload_queue.append([local_path, upload_client])
        self.closeMeun()

    def cancelSelectAll(self):
        #取消全选
        Button(
            self.frame1_2, image=self.choose_image, command=self.selectAll
        ).grid(row=2, column=0, sticky=N + E + S + W)
        self.isSelectAll = False
        self.select_list.clear()

    # @ 刷新按钮
    def flush(self):
        self.removeFileListPage()
        self.showObjectPageInNowPath(self.now_path)
        self.closeMeun()
        self.cancelSelectAll()


    # ^回到顶部按钮
    def goHomePage(self):
        if self.now_path == self.root_path:
            self.flush()
            return
        self.now_path = self.root_path
        self.removeFileListPage()
        self.showObjectPageInNowPath(self.now_path)
        
        # 更改显示栏        
        self.flushPathLable()
        self.closeMeun()
        self.cancelSelectAll()
    
    def newFolder(self):
        self.closeMeun()

        new_folder_ui = renameWindow.RenameUi('新建文件夹')
        self.root.wait_window(new_folder_ui)
        new_folder = new_folder_ui.getName()
        if new_folder == '':
            return

        for item in self.remote_filesname_list:
            if item['$f'] == new_folder:
                show_message_ui = showMessage.ShowMessage()
                show_message_ui.conflict('命名冲突了( ⊙ o ⊙ )啊！')
                return

        self.createNewFolder(new_folder)
        self.flush()

    def createNewFolder(self, new_folder):
        new_folder_path = self.now_path + '/' + new_folder
        rename_client = load.Load()
        rename_client.mkdir(new_folder_path)

    # 调整文件大小的表达
    def modifySizeNameFromFile(self, file_size):
        file_size = int(file_size)
        if file_size > 1024:
            file_size = file_size / 1024
            if file_size > 1024:
                file_size = file_size / 1024
                if file_size > 1024:
                    file_size = file_size / 1024
                    file_size = str(round(file_size, 2)) + 'GB'

                else:
                    file_size = str(round(file_size, 2)) + 'MB'
            else:
                file_size = str(round(file_size, 2)) + 'KB'
        else:
            file_size = str(round(file_size, 2)) + 'B'

        return file_size

    # 调整修改时间
    def timeStampToTime(self, timestamp):
        timeStruct = time.localtime(timestamp)
        return time.strftime('%Y-%m-%d %H:%M:%S', timeStruct)

    # 配置滚轮
    def OnFrameConfigure1_3(self, event):
        self.canvas1_3.configure(scrollregion=self.canvas1_3.bbox("all"))


    def removeFileListPage(self):
        if self.frame1_3 != None:
            self.frame1_3.destroy()
            self.canvas1_3.destroy()
            self.vsb1.destroy()
            self.remote_filesname_list.clear()

    # 更改文件路径显示栏
    def flushPathLable(self):
        if self.dfiles_num == 0:
            self.path_label["text"] = self.home_text + self.now_path + '(空文件夹)'
        else:
            self.path_label["text"] = self.home_text + self.now_path

    def finishSign(self):
        while True:
            if os.path.exists(self.token_file_path):
                self.canvas1_1.destroy()
                self.user_label["text"] = '百度网盘客户端'
                self.setLogButton()
                self.showFileListPage()
                break
            time.sleep(1)

    def setLogButton(self):
        Button(
            self.frame1, text='注销登录', width=10,
            font=('Arial', 10),
            command = self.logout
        ).grid(row=0, column=15, sticky=N + E + S + W)

    def showSignPage(self):
        self.canvas1_1 = Canvas(self.root)
        self.frame1_1 = Frame(self.canvas1_1)
        self.canvas1_1.pack(fill='both')
        self.canvas1_1.create_window((0, 0), window=self.frame1_1)
        self.frame1_1.pack(fill='both')

        t = threading.Thread(target= self.getSign)
        t.setDaemon(True)
        t.start()

        Label(self.frame1_1,
              text = '请访问终端中网址，并粘贴回授权码到终端中',
              font=('Arial', 15),
              width=100 ,
              anchor=W,
              ).grid(row=1, padx=10,  sticky=N + E + S + W)

        Label(self.frame1_1,
              text = '授权可能需要5分钟，授权成功就可以愉快的使用~\(≧▽≦)/~啦啦啦',
              font=('Arial', 15),
              width=100 ,
              anchor=W,
              ).grid(row=2, padx=10,  sticky=N + E + S + W)

    def getSign(self):
        self.sign_url_load = load.Load()

    def logout(self):
        logout_ui = logout.Logout()
        self.root.wait_window(logout_ui)
        is_logout = logout_ui.getLogout()
        if is_logout:
            os.remove(self.token_file_path)     # 慎用
            self.root.destroy()
        else:
            return

    def show(self):
        self.setWindow()
        # 判断登录
        if os.path.exists(self.token_file_path):
            self.showFileListPage()
        else:
            self.showSignPage()

        t = threading.Thread(target=self.finishSign)
        t.setDaemon(True)
        t.start()

        try:
            self.root.mainloop()
        except :
            pass


if __name__ == '__main__':
    driver = DriverUi()
    driver.show()
