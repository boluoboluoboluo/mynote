### 客户端

code：

```py
from ftplib import FTP
 
# FTP服务器的IP地址或主机名
ftp_server = '127.0.0.1'
# FTP服务器的用户名和密码
username = 'user'
password = '12345'
 
# 连接到FTP服务器
ftp = FTP()
ftp.encoding = 'utf-8'  # 编码
ftp.connect(ftp_server, 21)		#ip port
ftp.login(username, password)
 
print(ftp.getwelcome())  # 打印欢迎消息
 
# 显示当前工作目录
print('当前工作目录: %s' % ftp.pwd())
 
# 更改工作目录
# ftp.cwd('path/to/directory')
 
# 显示目录列表
files = ftp.nlst()
print('目录列表: %s' % str(files))
 
# 下载文件
# ftp.retrbinary('RETR path/to/file', open('local_file_path', 'wb').write)
# ftp.retrbinary('RETR 1.html', open('./a.html', 'wb').write)	#示例
 
# 上传文件
# ftp.storbinary('STOR path/to/file', open('local_file_path', 'rb'))
 
# 断开连接
ftp.quit()
```

### 服务端

```sh
#需先安装
pip install pyftpdlib
```

code：

```py
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
 
# 创建一个DummyAuthorizer来管理用户账号
authorizer = DummyAuthorizer()
 
# 添加一个用户，参数依次是：用户名，密码，主目录，权限
authorizer.add_user('user', '12345', './file/', perm='elradfmwMT')
 
# 将所有用户写权限设置为开启
authorizer.add_anonymous('./file/', perm='elradfmwMT')
 
# 开启DummyAuthorizer
handler = FTPHandler
handler.authorizer = authorizer
 
# 设置FTP服务器的地址和端口
server = FTPServer(('127.0.0.1', 21), handler)
 
# 开始运行FTP服务器
server.serve_forever()
```

