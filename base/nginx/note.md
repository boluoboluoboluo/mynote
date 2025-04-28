

#### 安装

```sh
# debian系统

sudo apt update
sudo apt install nginx	#安装

sudo apt show nginx 	#查看
sudo systemctl status nginx 	#查看运行状态

# 配置文件：
/etc/nginx/nginx.conf
```



#### 源码安装

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



#### 上传413问题

上传报错：`413 Request Entity Too Large`

解决方法：

打开nginx主配置文件`nginx.conf`， 找到`http{}`段并修改以下内容：

```nginx
http{
    client_max_body_size 100m;		#根据需要设置
}
```



