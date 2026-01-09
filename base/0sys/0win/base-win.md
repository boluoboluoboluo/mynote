访问终端方式：

1. 开始运行：输入cmd，回车		#管理员运行ctrl+shift+enter
2. win+R，输入cmd，回车

### 系统

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

shutdown /l		#注销
shutdown /s /t 0	#关机
shutdown /r /t 0	#重启

ping  域名
ping -a ip		#查看指定ip的主机名
ipconfig /all
arp -a 			#查看mac地址

ipconfig /displaydns
ipconfig /displaydns > c:/z_dns.txt
ipconfig /flushdns

net start telnet	#开启telnet服务

net start		#查看开启了哪些服务
net session		#查看网络会话

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



#防火墙开放端口：添加入站规则

```

#### 运行相关

```sh
win+r 打开运行框,输入:
control		#打开控制面板
msconfig 	#打开启动项
services.msc	#打开服务
regedit		#打开注册表
calc		#计算器
mspaint		#画图
eventvwr.msc	#事件日志
gpedit.msc 		#组策略
mstsc			#远程桌面
taskschd.msc	#任务计划
devmgmt.msc		#设备管理器
dxdiag			#查看显卡
wf.msc			#防火墙
sysdm.cpl		#系统属性
```



#### 服务相关命令

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

### 用户

```sh
whoami		#当前用户

net user 		#显示本机所有用户
net localgroup	#查看用户组


#隐藏用户

#cmd下切换用户：
runas /user:用户名 cmd
```



### 文件

```sh
dir						#显示当前目录内容
cd file_path		  	#切换目录
cd /d D:				#切换磁盘,或者 直接输入 D:
mkdir newfolder			#创建文件夹
type nul > newfile.txt	#创建文件 或者清空文件
echo 123 > newfile.txt	#写入文件,不存在则创建
echo 456 >> newfile.txt	#追加内容 会添加换行符
del newfile.txt			#删除文件
rmdir newfolder			#删除文件夹
rmdir /s newfolder		#删除非空文件夹	/q 参数:删除前不确认
copy file.txt distdir	#复制文件
xcopy folder1 folder2 /s /e  #复制文件夹 /s表示复制子文件和子文件夹(除了空的) /e表示复制空目录
move file|dir distdir	#移动文件或目录
ren file|dir newfile|newdir	#重命名文件或文件夹
type file.txt			#查看文件
more file.txt			#分页显示文件内容
attrib +h file.txt		#隐藏文件	删除隐藏文件需要先去掉该属性
attrib +s file.txt		#标记为系统文件
attrib +r file.txt 		#设置只读

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

#如果路径或文件名包含空格，必须用双引号括起来。

#符号链接
mklink

#查看文件关联，修改
assoc
	#示例：
	assoc .txt		#查看txt文件的关联方式
	assoc .txt=		#删除关联方式
	assoc .txt=txtfile	#重置关联方式
	
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



### 网络

```sh
net view 		#显示当前域中的计算机
net use			# 使用网络发现

arp -a			# 查看ARP表（IP与MAC地址对应）

tracert 目标主机或ip		#跟踪数据包节点

netstat -ano		#显示端口
netstat -anb		#显示端口，以及程序

#显示和修改本地IP路由表。
route print			#显示路由表。
route add [目标网络] mask [子网掩码] [网关]	#添加路由。
route delete [目标网络]		#删除路由。

#获取适配器名称
netsh interface show interface
# 禁用网络适配器（需要先知道适配器名称）
netsh interface set interface "以太网" admin=disable
# 启用网络适配器
netsh interface set interface "以太网" admin=enable

# 示例输出：
# IPv4 地址 . . . . . . . . . . . . : 192.168.1.100
# 默认网关. . . . . . . . . . . . . : 192.168.1.1
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
```



#### 无线热点

```sh
管理员打开cmd:

#检查网卡是否支持(查看支持的承载网络是否为是)	#即查看是否支持开启热点
netsh wlan show drivers
#创建
netsh wlan set hostednetwork mode=allow ssid=YourHotspotName key=YourPassword
netsh wlan set hostednetwork mode=allow ssid=boluo888 key=99999999
#启动
netsh wlan start hostednetwork
#开启共享
	网络连接->当前上网的适配器设置->属性->共享: 勾选允许其他网络用户连接 | 选择上面创建的虚拟适配器(类似本地连接2..)
#停止热点
netsh wlan stop hostednetwork
#禁用热点功能（可选)
netsh wlan set hostednetwork mode=disallow		#删除适配器(重启生效)
#查看热点状态
netsh wlan show hostednetwork

#无法删除时,设备管理器卸载
#重置网络栈:#重启电脑
netsh winsock reset
netsh int ip reset
ipconfig /release
ipconfig /renew
ipconfig /flushdns
#如果还是无法删除,则注册表删除或重命名以下条目
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Wlansvc\Parameters\HostedNetworkSettings

#查看所有已保存的Wi-Fi配置文件（包括热点）
netsh wlan show profiles
#删除
netsh wlan delete profile name="你的热点名称"
```



### 其他

```sh
#防火墙重启
netsh advfirewall reset

#查看文件夹大小 实用技巧
dir /s | find "个文件"
```



#### 域名解析

```sh
nslookup    	#交互式命令

#示例：
>server 192.168.1.1		#指定域名解析服务器
>set q=A				#指定资源类型
>www.baidu.com

#查询公网ip
nslookup myip.opendns.com resolver1.opendns.com
curl ifconfig.me	#同上
```



#### 批处理

```sh
#命令行传参
%1，%2，%3...	#接收
```





















