



访问终端方式：

1. 开始运行：输入cmd，回车		#管理员运行ctrl+shift+enter
2. win+R，输入cmd，回车

#### 系统

命令：

```sh
#命令 /?	#查看命令帮助
cls		#清屏

#系统信息
systeminfo		#查看操作系统信息
msinfo32		#查看系统运行情况
hostname		#机器名

#wmic模式：cmd下输入wmic
memorychip		#查看内存
cpu get *		#查看cpu

#查看主板信息：
wmic baseboard get product,manufacturer,version,serialnumber /format:list


#cmd下切换用户：
runas /user:用户名 cmd

ping  域名
ping -a ip		#查看指定ip的主机名
ipconfig /all
arp -a 			#查看mac地址

ipconfig /displaydns
ipconfig /displaydns > c:/z_dns.txt
ipconfig /flushdns

tracert 路由

netstat -ano		#显示端口
netstat -anb		#显示端口，以及程序
net start telnet	#开启telnet服务

net user 		#显示本机所有用户
net view 		#显示当前域中的计算机

net start		#查看开启了哪些服务

sc delete 服务名		#删除服务

#查看进程 
tasklist /svc
#结束进程
#以 进程ID 结束 
cmd: taskkill /pid 1 /T /F
# 以 进程名 结束 
cmd: taskkill /im notepad.ext /T /F
#注: 
/T = 以树形结束 
/F = 强制结束

#查看进程详细：
#cmd下输入wmic 进入wmic
#再输入process 列出进程及所在的目录

cacls *.*  	#查看目录权限
attrib *.* 	#查看目录文件属性

#防火墙开放端口：添加入站规则

```

#### 服务相关命令

```sh
net start		#列出正在运行的服务

net start 服务名 	#启动 
net stop 服务名	#停止

#sc命令：
sc config 服务名 start= demand 	#手动
sc condig 服务名 start= auto 		#自动
sc config 服务名 start= disabled 	#禁用
sc start 服务名	#启动
sc stop 服务名		#停止

sc delete 服务名	#卸载服务
```

#### 环境变量

```sh
#查看
set

#查看某个环境变量,如path
path
#或
echo %path%

#添加,编辑（当前命令行有效
set a=1		#添加一个a的环境变量 a=1
set a=%a%2	# a=12
#删除
set a=


#设置用户环境变量	会添加注册表
setx
#设置系统环境变量	会添加注册表
setx /M

```

#### 文件

```sh


#查看文件关联，修改
assoc
	#示例：
	assoc .txt		#查看txt文件的关联方式
	assoc .txt=		#删除关联方式
	assoc .txt=txtfile	#重置关联方式
```



#### 域名解析

```sh
nslookup    	#交互式命令

#示例：
>server 192.168.1.1		#指定域名解析服务器
>set q=A				#指定资源类型
>www.baidu.com
```



#### 批处理

```sh
#命令行传参
%1，%2，%3...	#接收
```





















