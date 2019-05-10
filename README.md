# bpcloud
## 基于Python原生库tkinter和houtianze大神的bypy实现的一个百度云Linux可视化客户端
作品安装说明：
请在对百度网盘未有限制或封禁的网络情况下使用。

## Linux（以Ubuntu16.04为例）：
### 在文件夹bpcloud下./bpcloud.sh进行认证，如果未使用过百度网盘可以首先申请百度网盘账号。认证时间5分钟以内
关闭终端后./bpcloud.sh即可使用
## 源码安装
在bpcloud-src文件夹下
Linux：
sudo apt install python3-tk
sudo apt install python3-pip
pip3 install requests_toolbelt
pip3 install configparser

## 使用说明：
源码安装在GUI文件夹下python3 bpcloud.py
请按照弹出窗口拷贝连接到浏览器获取认证码并拷贝到终端中确定开始使用
客户端的根目录页面是百度网盘的我的应用数据下/bypy

## 操作
可以在客户端实现文件、文件夹的移动，删除，拷贝，上传，下载，重命名，新建文件夹等。可以并行（可选择覆盖）下载文件。
用户第一次登陆之后可后免登陆，但是注销用户后按照上述说明请重新认证。

如果无法使用，请先检查网络，Linux可在bpcloud/log中查看日志信息。
