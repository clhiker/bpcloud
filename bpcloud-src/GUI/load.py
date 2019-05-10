# 文件列表信息	ok
# 上传下载进度	可以不去调用他的部分
# gui

# 登录注册
# 并发上传下载问题

import os
import sys
import showMessage
import time

sys.path.append("..")
from bypy.bypy import ByPy

class Load:
	def __init__(self):
		self.bp = ByPy()
		self.process = 0
		self.download_size = 0
		self.local_path = ''
		self.remote_path = ''
		self.remote_size = ''


	def setLocalPath(self, local_path):
		self.local_path = local_path
	def getLocalPath(self):
		return self.local_path
	def setRemotePath(self, remote_path):
		self.remote_path = remote_path
	def getRemotePath(self):
		return self.remote_path
	def setRemoteSize(self, remote_size):
		self.remote_size = remote_size
	def getRemoteSize(self):
		return self.remote_size

	def getFilesList(self, path):
		print(path)
		self.bp.list(path)
		# 返回一个字典列表
		return self.bp.fileslist

	def download(self, remote_path, local_path, finish_download_queue):
		load_sign_ui = showMessage.ShowMessage()
		load_sign_ui.beginWindow('下载')
		self.bp.download(remote_path, local_path)
		load_sign_ui = showMessage.ShowMessage()
		load_sign_ui.finishWindow('下载')
		filename = remote_path[remote_path.rfind('/') + 1 : ]
		finish_time = time.strftime("%Y-%m-%d %H:%M", time.localtime())
		file_size = os.path.getsize(local_path)
		finish_download_queue.append((local_path, filename, file_size, finish_time))


	def upload(self, local_path, remote_path):
		load_sign_ui = showMessage.ShowMessage()
		load_sign_ui.beginWindow('上传')
		self.bp.upload(local_path, remote_path)
		load_sign_ui = showMessage.ShowMessage()
		load_sign_ui.finishWindow('上传')


	def remove(self, remotepath):
		self.bp.remove(remotepath)

	def rename(self, old_path, new_path):
		self.bp.rename(old_path, new_path)

	def mkdir(self, remotepath):
		self.bp.mkdir(remotepath)

	def getRemoteFileSize(self, remote_up_path, filename):
		files_list = self.getFilesList(remote_up_path)
		for item in files_list:
			if item['$t'] == 'F' and item['$f'] == filename:
				return item['$s']

	def getLocalFileSize(self, localpath):
		return os.path.getsize(localpath)

	def move(self, old_path, new_path):
		self.bp.move(old_path, new_path)

	def copy(self, old_path, new_path):
		self.bp.copy(old_path, new_path)

	def getLoadProcess(self):
		return self.bp.getDownLoadProcess()

	def getDownloadSize(self):
		size = self.bp.getDownloadSize()
		return str(size)

	def getFinishDownload(self):
		return self.bp.getFinishDownload()

	def help(self):
		self.bp.help('command')

	# 清除用户登录信息
	def clear(self):
		os.remove(self.bp.getTokenFilePath())

	def getAuterPath(self):
		return self.bp.getTokenFilePath()

	def changeState(self, state):
		self.bp.setState(state)


	# # 获取登录的url
	# def getSignUrl(self):
	# 	return self.bp.getSignUrl()

	def sign(self):
		pass

if __name__ == '__main__':
	bypy = ByPy()
	bypy.list()