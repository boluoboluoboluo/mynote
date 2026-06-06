

#### 安装

```sh
# debian系统

sudo apt update
sudo apt install nginx	#安装

sudo apt show nginx 	#查看
sudo systemctl status nginx 	#查看运行状态

# 配置文件：
/etc/nginx/nginx.conf

sudo nginx -t	#检查配置文件语法
```

##### 源码安装

```sh
# debian系统

# 安装必要的依赖项
sudo apt update
sudo apt install build-essential libpcre3 libpcre3-dev zlib1g zlib1g-dev libssl-dev

# 1.下载源码
wget http://nginx.org/download/nginx-xx.xxx.xx.tar.gz
# 2.解压
tar -zxvf nginx-xx.xxx.xx.tar.gz
# 3.进入目录，配置
cd nginx-xx.xxx.xx
./configure
# 4. 编译和安装 Nginx
make
sudo make install


# 说明
# 默认情况下，Nginx 将被安装到 /usr/local/nginx
# 可以通过以下命令启动 Nginx：
sudo /usr/local/nginx/sbin/nginx

# 添加环境变量
vim ~/.bash_profile		#文件末尾添加如下内容:
NGINX_HOME=/usr/local/nginx/sbin
PATH=$PATH:$NGINX_HOME
export PATH

# 加载环境变量
source ~/.bash_profile

#查看
whereis nginx
```

##### 卸载

```sh
# 1.关闭nginx进程
./nginx -s stop
# 2.删除安装文件
rm -f /usr/local/nginx
# 3.清除安装包编译环境,安装包目录执行：
make clean
```



#### 信号控制

```sh
#linux命令行操作

#信号：
TERM/INT		#立即关闭
QUIT			#优雅的关闭
HUP				#重读配置文件使新配置生效
USR1			#重新打开日志文件，可用来进行日志切割
USR2			#平滑升级到最新版的nginx
WINCH			#所有子进程不接收处理新连接，相当于给work发送quit指令

#示例
ps -ef | grep nginx	#进程查询
kill -TERM PID		#立即关闭指定pid的进程
kill -INT `cat /usr/local/nginx/logs/nginx.pid`		#关闭nginx
kill -USR1 `more /usr/local/nginx/logs/nginx.pid`	#重新打开日志文件

#以下2句进行平滑升级：
#会生成新的master进程，pid写入nginx.pid,旧的pid写入到nginx.pid.oldbin
kill -USR2 `more /usr/local/nginx/logs/nginx.pid`
#kill旧的pid
kill -QUIT `more /usr/local/nginx/logs/nginx.pid.oldbin`

```

#### 命令

```sh
nginx -h		#帮助
nginx -v		#版本
nginx -V 		#详细信息
nginx -t		#检测nginx.conf语法是否有错误
nginx -s SIGNAL	#信号
	#SIGNAL:
	stop	#快速关闭
	quit	#优雅关闭
	reopen	#重新打开日志文件，类似于USR1信号
	reload	#类似于HUP信号
	
```

#### 版本平滑升级

**方式一**：信号升级

```sh
# 1.旧版备份/usr/sbin/nginx
cp nginx nginx_old
# 2.新版nginx拷贝到/usr/sbin/nginx
    cd nginx-xx.xxx.xx		# 新版解压目录
    ./configure
    make	# 只编译
    cp nginx /usr/sbin/nginx	#拷贝
# 3.发送信号，启用新版
kill -USR2 `more /usr/local/nginx/logs/nginx.pid`
# 4.发送信号，关闭旧版
kill -QUIT `more /usr/local/nginx/logs/nginx.pid.oldbin`
```

**方式二**：make升级

```sh
# 1.旧版备份/usr/sbin/nginx
cp nginx nginx_old
# 2.新版nginx拷贝到/usr/sbin/nginx
    cd nginx-xx.xxx.xx		# 新版解压目录
    ./configure
    make	# 只编译
    cp nginx /usr/sbin/nginx	#拷贝
# 3.新版安装目录，执行：
make upgrade
```

#### 配置文件nginx.conf

```sh
#全局块，需重启服务器，而不是reload

#user指令语法：
user user[group]		#工作进程权限用户，默认nobody
user www;				#示例，设置一个用户www

master_process	off;	#是否启动工作进程，默认on
work_processes	2;		#启动的工作进程数量(num/auto)，默认1

daemon	on;				#是否以守护进程方式启动(on/off)，默认on
pid	filepath;			#指定master进程号id存储路径，默认/usr/local/nginx/logs/nginx.pid

#配置错误日志：
#位置：全局块，http，server，location
#日志级别：debug|info|notice|warn|error|crit|alert|emerg
error_log file[日志级别];	#默认值：logs/error.log error

#include指令：引入其他配置文件
#位置：any
include file;
```

```sh
#event块

#accept_mutex:用来设置nginx网络连接序列化
#off时，请求到来，work休眠进程唤醒，争抢处理权（惊群）
#on时，请求到来，work休眠进程挨个唤醒
accept_mutex on;		#(on/off)，默认值on

#multi_accept:是否允许同时接收多个网络连接
multi_accept off;		#(on/off)，默认off，建议on

#worker_connections:设置单个work进程最大连接数
worker_connections 512;		#默认512

#use：选中哪种事件驱动来处理网络消息
use <method>		#(select/poll/epoll/kqueue)根据操作系统确定

```

```sh
#http块

#默认2行配置：
include mime.types;
default_type application/octet-stream;

#default_type:用来配置nginx响应前端请求默认的mime类型
#位置：http，server，location
default_type text/plain;		#默认

#access_log:访问日志
#位置：http，server，location
access_log path[format[buffer=size]]	#语法
access_log logs/access.log combined;	#默认

#log_format:日志输出格式
#位置：http
log_format name [escape=default|json|none|] string...;	#语法
log_format combined "...";		#默认

#sendfile:传输文件，可提高文件传输性能
#位置：http，server，location
sendfile off;		#（on/off），默认off

#keepalive_timeout:	设置长连接超时时间
#位置：http，server，location
keepalive_timeout 75;		#默认值

#keepalive_requests:一个keep-alive使用的次数
#位置：http，server，location
keepalive_requests 100;		#默认
```

#### 其他

##### 说明

```sh
# 切割nginx日志: 	
nginx安装后logrotate.d/下会建立配置文件,执行切割,不用改

# 安装后,即启动了,并自启动状态,监听80端口
# 注意: nginx开启的时候默认在下面这个文件会开启80端口,请注意
etc/nginx/sites-enabled/default		#这是个软连接,删除即可
```



##### 性能补充

```sh
#进程数: 
worker_processes auto;		#和cpu核心一致,不用改
#最大连接数
events {
	worker_connections	1024;	#每个进程最大连接,默认768 或 1024,不用改
}
#长连接超时
keepalive_timeout			#默认65秒,不用改

#压缩
http {
	gzip on;				# 默认开启,不用改 (如果没开启,建议开启)
}
```

**日志优化** 

```sh
#如果你的网站访问量很大（比如有很多视频、图片请求），频繁的磁盘写入日志会拖慢服务器性能。
#你可以在你的独立配置文件中做如下优化：

# 1. 静态资源（js/css/图片）通常很安全，可以关闭它们的访问日志，减少 80% 的写入开销
location /static/ {
    alias /home/project/myapp/static/;
    access_log off; # 关闭静态资源访问日志
}

# 2. 动态请求开启日志缓冲区（Buffer）
# 告诉 Nginx 攒满 32KB 的日志或每隔 5 秒再统一写入磁盘，大幅提升 I/O 性能
access_log /var/log/nginx/blobvideo_access.log combined buffer=32k flush=5s;

```

##### 安全小知识

```sh
#隐藏版本号

# 在 http 块中添加
server_tokens off;

============================
#禁止通过 IP 直接访问网站：防止恶意域名解析到你的服务器 IP，或者黑客直接用 IP 探测你的站点。

# 添加一个默认的 server 块，直接返回 443 或 400
server {
    listen 80 default_server;
    server_name _;
    return 443;
}
============================
# 限制请求体大小：防止黑客通过上传超大文件使服务器内存崩溃（DOS 攻击）。

# 限制上传文件最大为 10MB，根据业务调整
client_max_body_size 10m;


# 关闭上传目录执行权限
location /uploads/ {
    # 强制不解析 PHP 脚本，直接返回 403
    location ~ .*\.(php|php5|sh|py|pl|rb)$ {
        deny all;
    }
}

```

##### 超时

```sh
#nginx超时				  
# 默认60s
--proxy_read_timeout 60s;	# 超过 60 秒没有返回任何数据，Nginx 会主动断开，并向前端返回 504 Gateway Timeout
--proxy_connect_timeout 60s;	#Nginx 尝试连接后端的 Gunicorn，如果 60 秒都连不上（通常是后端挂了或队列满了），直接断开
--client_header_timeout 60s; / client_body_timeout 60s;#前端在上传超大视频时，如果因为网络太卡，导致连续 60 秒内没有向 Nginx 发送任何一个数据包，Nginx 就会断开请求
```

##### www-data用户

```sh
# 说明
在 Ubuntu、Debian 等系统上，当你使用 apt 安装 Apache 或 Nginx 时，系统会自动创建并调用 www-data 用户来运行这些网页服务

# 家目录
/var/www

# 不能用来登录
它的默认 Shell 通常被设置为 /usr/sbin/nologin 或 /bin/false。这意味着任何人都无法通过密码或 SSH 远程登录到 www-data 账户
```



##### 上传413问题

上传报错：`413 Request Entity Too Large`

解决方法：

打开nginx主配置文件`nginx.conf`， 找到`http{}`段并修改以下内容：

```nginx
http{
    client_max_body_size 100m;		#允许上传文件大小,根据需要设置
}
```



