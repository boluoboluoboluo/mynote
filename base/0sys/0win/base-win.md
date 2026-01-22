访问终端方式：

1. 开始运行：输入cmd，回车		#管理员运行ctrl+shift+enter
2. win+R，输入cmd，回车

### 系统

命令：

```sh
#命令 /?	#查看命令帮助
cls		#清屏

#系统信息
systeminfo		#查看操作系统版本信息,bios版本信息,补丁等
msinfo32		#查看硬件,软件,组件汇总
hostname		#机器名

#wmic模式：cmd下输入wmic
memorychip get *	#查看内存
cpu get *			#查看cpu
diskdrive get * 	#查看硬盘
wmic cpu get name, numberofcores	#查看cpu名称和核心数
wmic bios get smbiosbiosversion		#查看 BIOS 版本。
wmic bios get serialnumber			#查看序列号
#查看主板信息：
wmic baseboard get product,manufacturer,version,serialnumber /format:list


powercfg /l		#查看电源计划
---------------------------
shutdown /l		#注销
shutdown /s /t 0	#关机
shutdown /r /t 0	#重启
/f	#强制
/a	#终止
---------------------------
wmic product get name	#查看安装的软件列表
wmic product where name="Example" call uninstall	#卸载
---------------------------
bcdedit 	#管理引导加载程序

#安全模式
重启时按住shift

#用户账户控制 (调整 UAC 级别)
UserAccountControlSettings
--------------------------
chkdsk C: /f		#扫描并修复逻辑错误。
sfc /scannow		#扫描并修复受损的系统核心文件。
```

#### 运行相关

```sh
win+r 打开运行框,输入:
control			#打开控制面板
taskmgr			#任务管理器
msconfig 		#打开启动项
services.msc	#打开服务
regedit			#打开注册表
calc			#计算器
mspaint			#画图
eventvwr.msc	#事件日志
gpedit.msc 		#组策略
mstsc			#远程桌面
taskschd.msc	#任务计划
devmgmt.msc		#设备管理器
dxdiag			#查看显卡
ncpa.cpl		#网络连接
wf.msc			#防火墙
sysdm.cpl		#系统属性
resmon			#资源监视器
perfmon			#性能监视器
cleanmgr		#磁盘清理	设置 -> 存储 -> 存储感知：自动清理临时文件
lusrmgr.msc		#管理本地用户和组（家庭版不支持）
diskmgmt.msc	#磁盘管理

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
setx NAME VALUE
#设置系统环境变量	会添加注册表
setx NAME VALUE /M
```

### 服务

```sh
net start		#列出正在运行的服务	或者 win+r 输入:services.msc

#创建服务(管理员运行) 示例
sc create MyService binPath= "C:\Path\to\your\program.exe" start= auto

net start 服务名 	#启动 
net stop 服务名	#停止

#sc命令：
sc config 服务名 start= demand 	#手动
sc condig 服务名 start= auto 		#自动
sc config 服务名 start= disabled 	#禁用
sc start 服务名	#启动
sc stop 服务名		#停止
sc query servicename	#查询

sc delete 服务名	#卸载服务		#不包括配置和日志文件
```

### 进程

```sh
tasklist		#查看进程 
tasklist /svc	#进程及对应的服务
#结束进程
#以 进程ID 结束 
taskkill /pid 100 /T /F		#杀掉id为100的进程
cmd: taskkill /im notepad.ext /T /F
	/pid	#根据id
	/im		#进程名
	/T 		#以树形结束 
	/F 		#强制结束
---------------
```

### 用户

```sh
whoami			#当前用户
whoami /all		#查看完整用户信息

net user 		#显示本机所有用户
net localgroup	#查看用户组

#隐藏用户

#cmd下切换用户：
runas /user:用户名 cmd
-----------------
net user newuser password /add		#新增用户newuser
net user newuser /delete			#删除用户newuser
net user /active:yes		#启用, 禁用:no

net localgroup administrators newuser /add	#添加用户到管理员
-----------------
logoff		#注销当前用户
```

### 文件

```sh
#如果路径或文件名包含空格，必须用双引号括起来

#目录
dir						#显示当前目录内容
dir /a		#查看隐藏文件
dir /s | find "个文件"		#查看文件夹大小 实用技巧

cd file_path		  	#切换目录
cd /d D:				#切换磁盘,或者 直接输入 D:

mkdir newfolder			#创建文件夹
rmdir newfolder			#删除文件夹
rmdir /s newfolder		#删除非空文件夹	/q 参数:删除前不确认
copy file.txt distdir	#复制文件
xcopy folder1 folder2 /s /e  #复制文件夹 /s表示复制子文件和子文件夹(除了空的) /e表示复制空目录
-------------------------
#文件
type nul > newfile.txt	#创建文件 或者清空文件
echo 123 > newfile.txt	#写入文件,不存在则创建
echo 456 >> newfile.txt	#追加内容 会添加换行符
del newfile.txt			#删除文件
/f	强制
/q	安静模式

move file|dir distdir	#移动文件或目录
ren file|dir newfile|newdir	#重命名文件或文件夹
type file.txt			#查看文件
more file.txt			#分页显示文件内容

attrib +h file.txt		#隐藏文件	删除隐藏文件需要先去掉该属性
attrib +s file.txt		#标记为系统文件
attrib +r file.txt 		#设置只读
---------------------
#符号链接
mklink
---------------------
fc file1 file2 			#比较2个文件
find "abc" file.txt		#查找文件内容

copy file1.txt + file2.txt file1.txt	#合并文件内容到file.txt
type file1.txt >> file2.txt				#将file1.txt的内容写入file2.txt
#输入多行内容
(echo aaa & echo bbb) >> file.txt		#写入多行
echo ^| file.txt		#输入特殊字符 使用^转义
echo. >> file.txt		#追加空行
echo %date% %time% >> file.txt	#追加当前日期
(set /p="aaa" < nul) >> file.txt		#写入内容(不写换行)
------------------

#查看文件关联，修改
assoc
	#示例：
	assoc .txt		#查看txt文件的关联方式
	assoc .txt=		#删除关联方式
	assoc .txt=txtfile	#重置关联方式
------------------	
#共享
net share 
```

```sh
cacls *.*  	#查看目录权限
attrib *.* 	#查看目录文件属性

#权限
icacls
# 禁止移动/删除:
icacls "D:\MyData\TargetFile.txt" /deny Everyone:(D)
icacls "D:\MyData\*" /deny Everyone:(D)		#目录下所有文件
	Everyone: 指所有用户。你也可以替换为具体的用户名。
	(D): 代表 Delete（删除）权限。
	效果:尝试移动文件时会提示“文件访问被拒绝”。
#恢复可移动/删除
icacls "D:\MyData\TargetFile.txt" /remove:d Everyone
	/remove:d: 表示移除之前设置的“拒绝(deny)”条目。

#彻底锁定（禁止移动、重命名及修改内容）:
icacls "D:\MyData\TargetFile.txt" /deny Everyone:(M)
	(M): 代表 Modify（修改）权限。勾选此项会同时禁止删除、移动和更改文件内容。
	
#即便你是管理员，一旦设置了 /deny Everyone:(D)，你也无法移动它。如果想移动，必须先执行上方的“恢复”命令。
```

### 磁盘

```sh
diskpart	#磁盘管理（常用于修复 U盘分区）
```



### 网络

#### 地址配置

```sh
#查看ip
ipconfig /all		#查看所有接口详细配置
	/release		#释放当前IP地址
	/renew			#重新获取ip地址
	/flushdns		#清理dns缓存
	/displaydns
	/displaydns > c:/z_dns.txt
#查看mac
getmac		#查看mac地址
	/v	#详细输出,包括名称
---------------------
#设置静态ip
netsh interface ip set address "本地连接" static <IP> <掩码> <网关>	#设置静态 IP
#示例:
netsh interface ip set address "Ethernet" static 192.168.1.10 255.255.255.0 192.168.1.1#设置静态内网 IP
#dhcp 动态ip
netsh interface ip set address "本地连接" dhcp	#切换到 DHCP

netsh winsock reset		#重置网络堆栈

#获取适配器名称
netsh interface show interface
# 禁用网络适配器（需要先知道适配器名称）
netsh interface set interface "以太网" admin=disable
# 启用网络适配器
netsh interface set interface "以太网" admin=enable
--------------------
```

#### 内网管理

```sh
#arp :查看和管理 ARP 缓存（IP 到 MAC 的映射）
arp -a 			#查看ARP表（IP与MAC地址对应
arp -d ip		#删除指定arp
arp -s ip mac	#添加静态arp
-------------
#route :查看和管理路由表，用于内网/互联网流量路由控制
route print		#显示路由表
route add <网络> mask <掩码> <网关> 	#添加路由
	route add 192.168.2.0 mask 255.255.255.0 192.168.1.1	#示例:添加内网路由
route delete <网络>	#删除路由
route change <网络> mask <掩码> <网关>	#修改路由

# 示例 ip:192.168.1.100  网关:192.168.1.1
# 添加环回路由（127.0.0.1）
route add 127.0.0.0 mask 255.0.0.0 127.0.0.1 -p
# 添加本地广播路由
route add 255.255.255.255 mask 255.255.255.255 127.0.0.1 -p
# 添加默认路由（访问互联网）
route add 0.0.0.0 mask 0.0.0.0 192.168.1.1 -p
# 添加本地网络路由
route add 192.168.1.0 mask 255.255.255.0 192.168.1.100 -p
# 添加组播路由
route add 224.0.0.0 mask 240.0.0.0 192.168.1.100 -p
# 添加本地广播路由（使用实际接口IP）
route add 255.255.255.255 mask 255.255.255.255 192.168.1.100 -p
--------------
```

#### 互联网管理

```sh
#查询公网ip
nslookup myip.opendns.com resolver1.opendns.com
curl ifconfig.me	#同上
```

```sh
#ping 测试连通
ping www.google.com		#示例
	-t 	#持续ping
	-n	#指定次数
	-l	#指定数据包大小(字节)
ping -a ip		#查看指定ip的主机名
-------------	
#tracert 路由跟踪
tracert www.google.com	#显示到目标的路由跳数和延迟 默认30跳
-------------
#nslookup 查询 DNS 记录，用于互联网域名解析管理 (可交互)
nslookup www.example.com	#查询域名 IP
	set type=MX		#切换查询类型（如 MX 邮件记录）
	server <DNS IP>	#指定 DNS服务器ip
#示例：
>server 192.168.1.1		#指定域名解析服务器
>set q=A				#指定资源类型
>www.baidu.com
--------------
#netsh wlan 管理无线网络链接（Wi-Fi）
netsh wlan show profiles		#查看所有 Wi-Fi 配置文件
netsh wlan show networks		#扫描可用网络。
netsh wlan connect name=<SSID>	#连接指定网络
	netsh wlan connect name="MyWiFi"	#示例:连接到指定 SSID	
--------------
```



#### 网络连接情况

```sh
#netstat 显示网络连接、路由表、接口统计和监听端口，用于查看活跃的内网/互联网链接和任务
	-a：显示所有连接和端口
	-n：数字格式（不解析主机名）
	-o：显示拥有进程 ID
	-b：显示进程名称（需管理员权限）
netstat -ano：查看所有连接和 PID
--------------------
#net use 查看和管理网络驱动器映射，用于内网文件共享链接
net use		#查看所有网络驱动器
net use Z: \\server\share	#映射 Z 盘到共享
net use Z: /delete			#删除 Z 盘映射

--------------------
net view 		#显示当前域中的计算机

net start		#查看开启了哪些服务
net start telnet	#开启telnet服务
net session		#查看网络会话
```

### 计划任务

```sh
schtasks /query		#查看任务列表

----------------
计划任务无法禁用时,先杀掉对应的进程
```

### 日志

```sh
wevtutil		#查询事件日志
wevtutil qe System /c:10 /f:text	#查看最近 10 条系统日志
/c:<数>	#数目
/f:text	#文本格式
```

