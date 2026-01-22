### 系统

#### 根文件系统

```sh
/boot: 系统启动相关的文件，如内核、initrd、grub（bootloader）
/dev: 设备文件
	块设备：随机访问，数据块
	字符设备：线性访问，按字符为单位
	设备号，主设备号，次设备号
/etc: 配置文件
/home: 用户家目录，每个用户一个目录/home/USERNAME
/root: 管理员的家目录
/lib: 库文件
	静态库： .a
	动态库： .so 	#.dll (win下)
	/lib/modules: 内核模块文件
/media: 挂载点目录，移动设别
/mnt: 挂载点目录，额外的临时文件系统
/opt: 可选目录，第三方程序的安装目录（旧，新的使用/usr/local目录）
/proc: 伪文件系统，内核映射文件
/sys: 伪文件系统，和硬件设备相关的属性映射文件
/tmp: 临时文件，/var/tmp
/var: 可变化的文件（如日志等），建议单独分区

#系统启动需要用到的程序
/bin: 可执行文件，用户命令
/sbin: 管理命令

#操作系统核心功能，可单独分区
/usr: shared, read-only
	/usr/bin
	/usr/sbin
	/usr/lib
	
/usr/local: 第三方软件的相关文件（不影响系统）
	/usr/local/bin
	/usr/local/sbin
	/usr/local/lib
```

#### 终端类型

```sh
console	#控制台
pty		#物理终端(VGA:显卡)
tty#	#虚拟终端(VGA)，#代表第几个虚拟终端
ttys	#串行终端
pts/#		#伪终端，（远程连接，通过ssh等方式）

#bash
tty		#显示当前使用的tty设备
echo "hello" >> /dev/pts/1		#向其他终端发信息，不（要轻易尝试向其他设备发数据！）
```

#### 系统信息（debian为准）

```sh
systemd-analyze blame	#查看启动耗时

shutdown -r now	#重启	如提示未找到命令，则前面加 sudo
shutdown -r 10	#10分钟后重启
shutdown -h now	#关机
shutdown -h 10	#10分钟后关机
-c	#取消

sudo reboot		#重启
sudo poweroff	#关机
---------------------
hostname 				#主机名 /etc/sysconfig/network
echo $HOSTNAME			#获取当前主机名
uname -a				#查看内核及发行版	或 cat /etc/os-release
cat /proc/version		#查看版本的命令
cat /proc/cpuinfo		#查看cpu信息
cat /proc/meminfo		#查看内存信息
lscpu #cpu详细信息
lsusb	#查看usb设备
lspci	#查看所有设备信息

sudo dmidecode -t bios	#查看bios
--------------------
free	#查看内存 -h 友好显示

top	#查看运行动态视图	
	# 按 e 内存可mb,gb,tb等友好显示
	# 按 shift+M 可以按内存大小排序

vmstat	#显示系统状态信息
vmstat 1 #每隔1秒显示1次
vmstat 1 5 #每隔1秒显示1次，共显示5次

iostat	#io压力
------------------------------
man 命令	#查看命令帮助
#快捷打开终端： `ctrl+alt+t`
#清屏幕：`ctrl+l` 或 命令clear
#锁屏快捷键
ctrl+alt+L
#锁终端
ctrl + S	#解锁:ctrl + Q
#终止进程
ctrl+c
#挂起进程
ctrl+z		#挂起当前进程到后台(占据内存-注意),使用jobs查看 

date	#系统时间
```

#### 环境变量

```sh
set 	#设置变量,当前进程有效
	--默认显示 所有环境变量+当前脚本/终端生效的私有变量	
	--范围:(全部)
export	#把普通变量导出为环境变量,使其被子进程(如在该终端启动的程序)继承
	--默认显示 环境变量+终端生效的变量
    --范围:(当前进程)
		 
env 	#临时设置环境变量  
	--默认显示 当前所有环境变量		#等于 export -p
	--范围:(跨进程)
	
unset varname	#删除当前生效的变量(环境变量+本地变量)
=====================
#相关文件
/etc/profile	#环境变量	   用户级别:~/.bash_profile
/etc/bashrc		#shell变量	用户级别:~/.bashrc
=====================
#添加环境变量,临时
sudo export PATH=/home/mppath:$PATH		#终端或进程退出失效
----------
#添加环境变量,永久
sudo vi /etc/profile	
	在文档最后，添加:
	export PATH="/home/tuotu/bin:$PATH"
source   /etc/profile	#使立即生效
----------
=====================
echo $PATH		#查看path环境变量
echo $LANG		#查看编码
echo $SHELL		#查看shell版本
```

### 服务

```sh
systemctl start 服务名			#启动服务
systemctl stop 服务名			#停止
systemctl restart 服务名		#重启
systemctl reload 服务名		#重载
systemctl enable 服务名		#自动启动
systemctl disable 服务名		#不自动启动
systemctl status 服务名		#服务状态

systemctl list-units 服务名		#列出所有
systemctl list-units --type=service	#查看所有服务
systemctl list-units --type=service --state=running	#查看正在运行的服务
systemctl list-unit-files --type=service --state=enabled	#查看开机自启的服务
```

### 进程

```sh
pstree	#进程树

ps -aux		#查看当前登录用户所有进程
-a 终端有关的进程
-u 启动进程的用户信息
-x 终端无关的进程
	
ps -ef		#列出进程及对应父进程
-e 显示所有进程
-f 所有格式

#查看系统前10内存
ps -aux --sort=-%mem | head -11

#只看 PID、进程名和物理内存RSS
ps -eo pid,comm,rss,%mem --sort=-rss | head -n 10		# -o 参数:指定格式
------------------------
kill 进程id	#杀死进程
killall 进程名	#根据进程名杀死进程

kill -l		#显示所有信号
	1：SIGHUP（让一个进程不用重启，就可以重读配置文件,并使其生效）
	2：SIGINT（ctrl+c，中断一个进程）
	9：SIGKILL（强行杀死一个进程）
	15:SIGTERM（终止一个进程，释放资源，默认信号）
	#示例：
		kill -1
		kill -SIGUP
--------------------------
pkill nginx			#杀死名字里带 nginx 的所有进程
pkill -9 chrome		#杀死所有进程及其子进程
pkill -f app.py		#杀死与其运行的某个脚本匹配的进程

sudo pkill -u testuser	#踢出用户
sudo pkill -t pts/1		#踢出正在使用pts/1终端的用户
------
#常用方式:
pgrep -a php	#列出匹配的进程和完整命令行
pkill php		#
------
```

**作业**

```sh
#作业
前台作业：占据命令提示符
后台作业：启动后，释放命令提示符，后续操作在后台完成
前台 -> 后台：
	ctrl+z：把正在前台的作业送往后台（此时stoped）
	COMMAND &：让命令在后台执行

jobs：查看后台所有作业
	作业号，不同于进程号
	+：命令默认操作的作业
	-：命令下一次操作的作业
	
bg ：让后台的停止作业继续运行
	#示例
	bg [%JOBID]	#默认为+号作业
	
fg ：重新调回前台
	#示例
	fg [%JOBID]	#默认为+号作业
	
kill %JOBID		#杀死后台作业
```

### 用户

用户管理

```sh
id		#查看当前用户,显示uid,gid及所属组
finger username	#查看用户相关信息

w		#查看当前系统中登录的用户,及正在干嘛
who 	#当前登录系统的用户
who -r	#显示当前运行级别
whoami	#当前用户

last	#最近登录及重启历史，显示的是/var/log/wtmp文件内容
last -n 3	#最近3次登录

lastlog	#每个用户上一次的登录
lastlog -u test	#显示test用户上一次登录

lastb	#显示用户错误的登录尝试，/var/log/btmp内容
lastb -n 3	#最近3次错误登录

sudo pkill -u username	#剔出某个登录用户
sudo pkill -9 -u 用户名  #剔除并杀死其所有进程
-------------------

#查看有哪些真人用户(拥有登录bash)
grep -E "/bin/bash|/bin/sh" /etc/passwd	

#添加
useradd		#创建用户
useradd -m	test	#常见方式,创建test用户,-m 同时创建家目录 
-d path		#创建时指定家目录
-u UID		#指定用户id
-g GID		#指定组id
-r 			#创建系统用户
-s path		#指定指定登录shell
-c "注释"	  #添加注释

adduser		#交互式创建
-------------------
#密码
passwd 		#当前用户设置密码	
sudo passwd username	#示例:给username用户设置密码
sudo passwd -d username	#删除密码,使其可无密码登录,(不推荐)
sudo passwd -l username	#锁定账户,禁止登录 -u 解锁
-------------------
#修改
sudo usermod -aG 组1,组2 用户名	  #常用,追加数组 -a表示追加(否则会覆盖)
sudo usermod -g 新组名 用户名	#修改属组

sudo usermod -l 新用户名 旧用户名	#修改用户名
sudo usermod -d /新路径 -m 用户名	  #修改主目录 -m 表示将原家目录文件一并迁移
sudo usermod -u 新ID 用户名			#改UID
sudo usermod -e YYYY-MM-DD 用户名	#设置过期时间
sudo usermod -c "新备注文字" 用户名	#改备注
-------------------
#删除
sudo userdel -r test		#常见方式,删除用户test及家目录
-------------
sudo su	#切换用户	不建议使用root用户
sudo -l	#检查当前拥有的sudo权限

#提权
vi /etc/sudoers
	--在行 %sudo ALL=(ALL:ALL) ALL 下面添加:
	xxx ALL=(ALL:ALL) ALL	#xxx 为需要 sudo 权限的用户名
=========================
#用户组

sudo groupadd groupname		#创建组

sudo groupmod -n new_name old_name	#修改组名
sudo groupmod -g 1010 groupname	#修改组id

sudo groupdel groupname		#删除组 注：如果该组是某个用户的主组，则无法直接删除

groups username 	#查看用户所属组

sudo gpasswd -d username groupname	#将用户移出组
=========================
#配置文件

/etc/passwd		#记录用户基本属性，每行对应一个用户 对所有用户都可读,7个字段 格式如下:
用户名:口令:用户标识号:组标识号:注释性描述:主目录:登录Shell
	--口令 	 #“x”或者“*” 真正口令在:/etc/shadow
	--户标识号 #取值范围0～65 535。0(超级用户root) 1～99由系统保留(管理账号)，
			  #普通用户的标识号从100开始。在Linux系统中，这个界限是500。
	--组标识	#对应/etc/group文件中的一条记录。

/etc/shadow
登录名:加密口令:最后一次修改时间:最小时间间隔:最大时间间隔:警告时间:不活动时间:失效时间:标志

/etc/group
组名:口令:组标识号:组内用户列表
=========================
#查看用户变动日志

grep "useradd" /var/log/auth.log	#示例
grep "something" /var/log/lastlog	#示例
```



### 文件

> 蓝色表示目录；
> 绿色表示可执行文件；
> 红色表示压缩文件；
> 浅蓝色表示链接文件；
> 白色表示其他文件；
> 黄色是设备文件，包括block, char, fifo。

```sh
#示例: ls -l 显示如下:
-rw-r--r-- 1 user group 1024 Jan 9 01:29 file.txt
列1:	权限与类型 
	第1位：-为文件，d为目录，l为链接。后9位：每3位一组，分别表示属主、属组、其他人的读(r)、写(w)、执行(x)权限。
	!!!注意:当x显示位s时,意味着特殊权限,即任何用户运行该程序,都会临时获得该文件所有者的权限!
列2: 硬链接数
	该文件被硬链接引用的次数。若是目录，通常指其包含的子目录数。
列3: 所有者 	#文件的属主用户名。
列4: 所属组 	#文件所属的用户组名。
列5: 文件大小	#默认单位为字节 (Bytes)。配合 -h 参数可显示为 KB/MB。
列6: 修改时间 	#文件最后一次内容被修改的时间
列7: 文件名 	#文件或目录的名称

#默认情况下，ls -l 只会对旧(通常是超过6个月)的文件显示年份。若想显示年份，用以下命令
ls -l --full-time
ls -l --time-style="+%Y-%m-%d %H:%M"	#自定义时间
```



#### 文件操作

```shell
#查看文件状态
stat filename
stat --format "%U"	filename	#只查看文件名

#查看文件类型
file filename
-------------------------
ls 	#列出目录，参数 -a:全部文件，-d：仅列出目录，-l：列出文件属性详情，-i：显示inode节点信息
ls -lh	#查看目录详情
ls | head -n1	#显示第一个文件名字
#查看目录树
tree 
#排序
sort file	#目录下文件进行排序
--------------------------
touch filename	#创建文件 touch命令可修改文件的访问时间和修改时间
cat [-AbEnTv] filename	#查看文件，参数 -A：列出特殊字符，-n：列出行号，-b：列出行号，空白行不显示行号
#less命令，查看文件，比more常用，可回翻
less filename 	# -N 参数显示行号
head -n 5 filename 	#显示文件开始5行
tail -f filename	#显示文件末尾，默认10行，-f参数：实时显示文件添加的内容
-------------------------
pwd	[-P] #显示当前目录，参数 -P：显示确实路径，而不是链接(link)路径

mkdir [-mp]	目录名称	#创建目录，参数 -m：配置权限，-p：递归创建所需要的目录

rmdir [-p] 目录名		#删除空目录，参数 -p:从该目录起删除多级空目录
mktemp -d			#自动生成随机目录名

cp [-adfilprsu] src dst	#复制文件或目录，参数 -i：存在则询问，-p：连同属性一起复制，-r：递归复制，-d：若为链接，复制链接属性而非文件，-a:等于-pdr
rm [-fir] 文件或目录		#移除文件或目录，-f：强制，-i：询问，-r：递归
mv [-fiu] src dst	#移动文件或目录，或修改名称 参数-f：强制，-i：询问，-u：src文件较新则升级

#查找文件 参见bash
find 目录 -name '文件名'

#根据inode 进入目录
cd "$(find . -inum 1234567)"
-----------------------
chgrp [-R] 属组名 文件名	#更改文件属组，-R：递归更改文件属组
chown [–R] 属主名 文件名	#更改文件属主
chown [-R] 属主名：属组名 文件名

chmod [-R] xyz 文件或目录	#更改文件权限，r:4,w:2,x:1。xyz代表用户|组|其他的rwx值的和
chmod u=rwx,g=rx,o=r  test1    # 修改 test1 权限
chmod  a-x test1		#去掉可执行权限

umask	#遮罩码，用于创建文件的默认权限（默认值减遮罩码，即默认权限）文件默认值666，目录默认值777
```

```sh

#文本统计
wc file
cat file | wc -l	#统计行数

#字符转化
tr ”a" "A" < file	#文件里的a换成A
```

**写权限定义**

```sh
#写权限 (w) 的含义：
文件的写权限： 决定你是否能修改这个文件的内容。
目录的写权限： 决定你是否能修改这个目录的列表（即：在该目录下创建新文件、重命名文件、或删除文件）。
```

**特殊权限**

```sh
#添加该权限后,非权限用户也可以执行
#运行某程序时，相应进程的属主是程序文件自身的属主，而不是启动者
#此权限风险大，谨慎使用 
suid		
chmod u+s filename	#给文件添加s权限，若文件有x权限，显示为s，否则显示S
	#示例显示：-rwsr-xr-x 1 root root 63736 7月  27  2018 /usr/bin/passwd

#属组，同上
sgid	

sticky	
	#在一个公共目录，可以创建删除自己的文件，但不能删除别人的文件
chmod o+t dirfile	#对目录添加sticky权限	
	
#权限数字表示 示例
chmod 1755 filename	#前面的1代表具有sticky权限
chmod 3755 filename	#前面的3代表具有suid权限和sticky权限
```



#### 压缩解压

```sh
tar	#归档工具 (通常先归档,再压缩)
-c	#创建归档
-f	file.tar	#指定归档文件
-x	#解开归档
-t	#不解开，仅查看文件列表

-z	#使用gzip方式压缩归档
-j	#使用bzip2方式
-J	#使用xz方式
	
#示例
tar -czvf archive.tar.gz file1 file2 #gzip方式压缩file1 file2 2个文件
tar -czvf test.tar.gz a.c   #压缩 a.c文件为test.tar.gz
tar -tzvf test.tar.gz 		#列出压缩的文件
tar -xzvf test.tar.gz 		#解压gz文件
```

```sh
#gzip 只能压缩文件， 压缩后 后缀.gz， 
gzip file	#压缩文件, file.gz 压缩后源文件被清除 ， 
	-d file.gz #解压缩，解压后file.gz被清除
	-num	#num为数字，1-9，指定压缩比，默认为6

#bzip2 压缩大文件更有压缩比 只能压缩文件，后缀.bz2
bzip2 file	#压缩文件，生成file.bz2，压缩后源文件被清除
	-d file.bz2 #解压缩，解压后file.bz2被清除
	-num	#num为数字，1-9，指定压缩比，默认为6
	-k		#压缩后保留源文件

#xz 只能压缩文件，后缀.xz 压缩更强悍
xz file	#压缩文件，生成file.xz，压缩后源文件被清除
	-d file.xz #解压缩，解压后file.xz被清除
	-num	#num为数字，1-9，指定压缩比，默认为6
	-k		#压缩后保留源文件

```

```sh
zip		#归档压缩,压缩后不删除源文件 压缩比小
zip file.zip file1 file2 ...	#压缩file1,file2...，到file.zip
zip -e file.zip file.txt 	#压缩前提示输入密码	(加密压缩无法隐藏文件名)

unzip file.zip		#解压
unzip file.zip -d dir	#解压到目标文件夹

unzip -l file.zip 	#只看内容,不解压
unzip -o file.zip 	#强制覆盖已有文件(默认会询问)
unzip -n file.zip 	#不覆盖已有文件(跳过已存在的)
unzip -p "pass" file.zip 	#解压有密码的压缩包
```

```sh
7z		#压缩 (默认最高压缩比)
7z a archive.7z file1.txt folder/	#-a : 添加

7z a secret.7z folder/ -p -mhe=on	#带密码,且隐藏文件名
	-p：交互式输入密码。
	-mhe=on：加密文件名，不输密码看不见内部列表。

7z a -v100m archive.7z folder/		#分卷压缩（每个包 100MB）会生成 .7z.001, .7z.002 等文件

7z x archive.7z		#解压并保持目录结构
	-x 代表 eXtract（按完整路径解压）
7z x archive.7z -o/path/to/directory/	#解压到指定目录 注意:-o 和路径之间没有空格
7z x archive.7z "document.pdf"		#解压特定的文件：

7z l archive.7z		#列出压缩包内容（不解压）
7z t archive.7z		#测试压缩包是否完整/损坏

7z u archive.7z file_updated.txt	#更新压缩包中的文件
7z a archive.7z folder/ -mmt=8		#指定多线程压缩（加快速度）
	-mmt=8 使用 8 个线程
```



#### 加密

```sh
#gpg加密
gpg -c xx.zip	
gpgconf --kill gpg-agent	#执行清理缓存密码,否则,解密时不需要输入密码
gpg -d filename.gpg > filename	#解密

gpg --no-use-agent -c a.zip	#或者禁用缓存方式加密


##ssl加密
# 加密文件
openssl enc -aes-256-cbc -salt -in data.txt -out data.txt.enc
# 解密文件
openssl enc -d -aes-256-cbc -in data.txt.enc -out data.txt

#给服务器发送加密数据
echo "Hello SSL" | openssl s_client -connect 127.0.0.1:443 -quiet
```



### 磁盘

#### 逻辑卷

```sh
逻辑卷		#LV 逻辑卷之和不能超过卷组边界，每个逻辑卷相当于一个分区
卷组		 #VG 多个物理卷的模拟整体
物理卷		#pv 物理盘区
物理块		#PE	默认4m

#物理卷
pvcreate	#创建物理卷
pvremove	#移除物理卷数据
pvscan		#扫描物理卷
pvs			#查看
pvdisplay	#显示物理卷详细
pvmove		#移动物理卷数据

#卷组
vgcreat		#创建卷组
...
vgextend	#扩展
vgreduce	#

#逻辑卷
lvcreate	#创建逻辑卷
...


#将LV格式化，挂载，就可以使用
```



#### 磁盘操作命令

```sh
# -k：以kb显示，-m：以mb显示，-h：以易阅读格式显示，-H：1000取消1024进位，-T：显示文件系统类型，-i：以inode数量显示
df -h	#显示磁盘情况
df -i	#显示inode使用情况
df /home	#显示/home目录所在分区
df -h -x tmpfs -x devtmpfs	#只看物理分区 (排除虚拟文件系统)


du filename		#检查空间使用量
# -h：易读格式，-s：列出总量
du -sh .			#查看当前目录总大小
du -sh * 			#常用,显示当前目录下各文件大小(包括目录的总大小)
du -sh .[^.]* *		#显示当前目录文件大小,包括隐藏文件
du -sh * | sort -hr	#显示当前目录文件,大小排序



#fdisk：用于磁盘分区
fdisk -l	#列出分区信息
fdisk -l /dev/sda	#查看某个设备

#分区
fdisk /dev/sda
	p	#显示当前硬盘分区（包括为保存的改动）
	n	#创建新分区
		e	#扩展分区
		p	#主分区
	d	#删除第一个分区
	w	#保存退出
	q	#不保存退出
	t	#修改分区类型（文件系统）
	l	#显示支持的所有类型

#内核识别的分区
cat /proc/partitions

#重读分区表命令,(用于创建分区后内核未识别)
partprobe

```

**挂载**

```sh
#查看挂载,相关命令：
mount
df -h
lsblk	#分区信息

#挂载 将文件系统关联到根目录
#语法：
mount 设备 挂载点
	设备：
		设备文件	 #示例 /dev/sda5
		卷标		  #示例 LABEL=""
		uuid		#示例 UUID=“”
	挂载点：	#目录
		要求：
			1.目录为被其他进程使用
			2.目录存在
			3.目录中原有文件将会被暂时隐藏
#挂载示例		
mkdir /mnt/hdc6		#创建目录
mount /dev/hdc6 /mnt/hdc6	#挂载后，通过挂载点访问设备

#卸载 语法：umount 设备 或 umount 挂载点
umount /dev/hdc6	#示例

#重新挂载
mount -o remount 设备 挂载点

#永久挂载：
修改 /etc/fstab
```

```sh
#挂载选项
mount 设备 挂载点
	-a	#挂载/etc/fstab文件中定义的所有文件系统
	-n	#默认情况每挂载一个设备，会把改在设备信息保存至/etc/mtab文件，使用-n选项则不写入
	-t FSTYPE	#指定正在挂载的文件系统类型（该选项可不用，会自动获取类型）
    -r	#只读挂载，挂载光盘常用此选项
    -w	#读写挂载，（默认）
    -o loop	#挂载本地回环设备
    
#挂载镜像
mount -o loop /home/xx.iso /mnt/test		#示例


#文件系统的配置文件
/etc/fstab		#开机时该文件里的文件系统会被自动挂载
	该文件字段：
		字段1	#要挂载的设备
		字段2	#挂载点
		字段3	#文件系统类型
		字段4	#挂载选项
		字段5	#转储频率（定义完全备份的时间间隔）
		字段6	#开机自检次序（只有根为1，0表示不检查）
		

#若设备无法卸载，查看被使用情况（验证进程正在使用的文件或套接字）
fuser -v /mnt/test		#示例，查看/mnt/test正在被哪些进程使用
fuser -km /mnt/test		#将访问的挂载点进程全部杀掉
```



#### 磁盘管理 

```sh
#真空
#盘片，柱面，磁道，扇区

#MBR 主引导记录  0盘片0磁道0扇区，不属于操作系统 共512byte
#446byte BootLoader 引导加载
#64byte
	#每16byte 标识一个分区，可通过指针形式指向扩展分区
#最后2byte Magic Number 标记MBR是否有效

#系统启动说明
1.开机
2.加载bios到内存
3.根据bios指定的启动设备,读取该设备的MBR
4.加载BootLoader到内存
5.加载分区操作系统内核到内存

#性能指标
#柱面，寻道时间，读写延时，转速
#柱面越靠外，读写速率高
#分区按柱面划分

#磁盘存储数据方式 metadata data
#通过metadata查找data
#文件系统 -> 分区
#文件系统
	#本质是一个软件，并不在分区
	#将分区划分为metadata和data部分
	#data部分以block为逻辑单元划分，block第1位标记是否已使用
	#metadata部分有1个块位图区域(block bitmap)，全局记录data区block使用情况
	#metadata的inode区域，记录文件存储索引信息，inode编号全局唯一
		#inode记录文件属性信息(大小，属主等，不包括文件名)
		#文件名在目录inode指向的block里记录
		#根目录由内核加载
	#metadata部分另有1个位图区域(inode bitmap)，记录inode区的使用情况
	
#metadata又以划分blcok group的形式管理data block
#metadata中又有super block 保存block的全局信息
#metadata中又有块组描述符（GDT），管理block group
#boot block 分区的第一个块（预留）
#block size,块大小，一般为 1024,2048,4096 (byte)



#分区
主分区最多4个
扩展分区最多1个
逻辑分区	#扩展分区指向的介质，可以有多个
```

#### 文件底层

```sh
#新建文件，保存
1.扫描空闲inode，占据一个
2.寻找目录inode，在其block里写入文件项(文件名及文件inode号)
3.根据文件大小，扫描data bitmap区，分配block

#删除文件
1.清除目录指向block的文件项（文件名和inode号）
2.inode bitmap 将该文件inode号标记0(未使用)
3.data bitmap 将文件分配的block位 标记为0
	文件粉碎机原理，将文件的data block区域随机覆盖
```

#### 链接文件

```sh
#硬链接
#与原文件指向同一个inode
#只能对文件创建，不能对目录
#不能跨文件系统
#ls -l 命令第二个字段表示文件被硬链接的次数
#当硬链接次数大于1，删除其中一个文件，并未真正删除

#软链接（符号链接）
#可对目录创建，可跨文件系统
#拥有新的inode，inode指向的data block为原文件的路径
#软链接文件权限都为777，能找到，但不一定能访问，取决于原文件权限

ln f1 f2          #创建f1的一个硬连接文件f2
ln -s f1 f3       #创建f1的一个符号连接文件f3 (软链接)
```

#### 设备文件

```sh
#块设备，按块为单位，随机访问的设备（如硬盘）
#字符设备，按字符为单位，线性设备（如键盘）

#主设备号，标识设备类型 ls -l /dev 第5个字段
#次设备号，标识同一类型的不同设备

#设备指具体硬件设备，一般由内核指定
#创建设备文件 示例
mknod mydev c 66 0	#在当前目录创建字符设备，主设备号66，次设备号0
	-m	#指定权限


#硬盘
IDE,ATA		#早期设备，hd开头
SATA,SCSI,USB		#sd开头
	a,b,c...区分同一类型的不同设备
	1,2,3,4	#主分区 示例：/dev/sda1
	5...	#逻辑分区	/dev/sda5
	
```

#### 文件系统

```sh
#内核功能，内核指定分区为某文件系统

#低级格式化：磁道
#高级格式化：创建文件系统
	mkfs -t ext3	#示例，格式化为ext3文件系统
	
#不同文件系统的底层系统调用不一样
#上层命令执行文件操作时需通过虚拟文件系统VFS,实现兼容操作

#常见文件系统
FAT32	#windows，在linux上叫做vfat
NTFS	#windows，在linux上支持不友好
ISO9660	#光盘
CIFS	#windows，网络邻居（也是文件系统）
ext2
ext3,ext4		#支持日志文件系统功能
xfs
reiserfs
jfs		#日志文件系统
nfs		#网路文件系统
ocfs2
gfs2
swap

```

**创建文件系统**

```sh
#查看当前内核支持的文件系统
cat /proc/filesystems		#nodev表示伪文件系统

#对分区创建文件系统
mkfs -t ext2 /dev/sda5		#示例，对分区/dev/sda5创建ext2类型的文件系统
mkfs -t vfat /dev/sda6		#示例

#专门管理ext系列文件系统命令
mke2fs /dev/sda5	#创建ext2文件系统
	-j 	#创建ext3文件系统
	-b 	#指定block size，默认4096，可用指1024，2048，4096
	-L	#指定卷标
	-m num	#指定预留大小，默认5%	#示例 -m 3	#指定3%
	-i	#指定inode大小，默认8192
	-N	#指定inode个数
	-F	#强制创建
	
#查看磁盘设备属性，uuid，type，label(卷标)等
blkid /dev/sda5		#查看分区属性

#查看或定义卷标
e2label	/dev/sda5

#调整文件系统相关属性，如类型，ext2调整为ext3
tune2f2 /dev/sda5
	-j 	#ext2升级为ext3 (无损调整，不能降级)
	-L	#设定卷标
	-m	#调整预留百分比 默认5%	#示例 -m 3	#指定3%
	-r	#指定预留块大小
	-o	#设定默认挂载选项
	-c	#指定挂载次数达到多少后进行自检，0或-1表示关闭
	-i	#挂载使用多少天后进行自检，0或-1表示关闭
	-l	#显示超级块中的信息
	
#显示文件系统相关信息
dumpe2fs /dev/sda5
	-h	#只显示超级块信息
	
#检查并修复文件系统
fsck 	/dev/sda5
	-t 	FSTYPE	#指定文件系统类型(可不指定)，示例：-t ext3
	-a		#自动修复
	
#专门修复ext系列文件系统命令
e2fsck	/dev/sda5
	-t	#强制检查
	-p	#自动修复
```

#### 虚拟内存

```sh
#单独的swap分区，在内存过载时应急使用

#查看
free	#查看物理内存和交换分区的使用情况
	-h	#友好显示查看
	
#创建swap分区
思路：
1.fdisk分区，并调整分区类型为82（linux/swap）
2.创建交换分区
	mkswap /dev/sda5	#示例
		-L	#指定卷标
3.启用交换分区
	swapon /dev/sda5	#示例

#关闭交换分区
swapoff /dev/sda5	#示例

#另一种方式创建swap分区（如果磁盘分区不够）
思路：
1.创建文件	#使用dd命令复制，dd表示复制数据流
	dd if=数据来源路径 of=数据复制路径	#示例：dd if=/test of=/home/test
		bs=1	#示例，block size大小
		count=2	#示例，block size数目
	dd if=/dev/zero of=/home/swapfile bs=1M count=1024
2.创建交换分区
	mkswap /home/swapfile	#示例
3.启用
	swapon /home/swapfile	#示例
	
	
#启用所有定义在/etc/fstab文件的交换设备
swapon -a
```



### 网络

#### 网络配置

```sh
#ip link 显示和管理网络接口链接状态，用于查看系统内部物理/虚拟链接列表、启用/禁用接口
ip link show	#查看所有接口列表和状态
ip link show eth0	#查看单个接口 eth0(名字) 的详情
ip link set <接口> up/down	#启用/禁用接口
	sudo ip link set eth0 down	#示例: 禁用接口（修改


sudo ip link add dummy0 type dummy	#新增虚拟接口dummy0(名称)
sudo ip link del dummy0				#删除虚拟接口
-------------------------
#ip addr 显示和管理 IP 地址配置，用于内网/系统链接的 IP 分配
ip addr show	#查看所有接口的 IP 列表
ip addr add <IP/掩码> dev <接口>	#设置 IP
	#示例
	sudo ip addr add 192.168.1.10/24 dev eth0	# 给ecth0网口设置ip为192.168.1.10
	sudo ip link set dev eth0 up	#使更改生效
sudo ip addr del 192.168.1.10/24 dev eth0	#删除特定 IP
sudo ip addr flush dev eth0			#清除接口所有 IP

#一块网卡可以有多个地址,示例:
eth0:0
eth0:1
------------------
nmcli device status		#查看所有设备列表

```

#### 内网管理

```sh
#arp 
arp -a 	#显示所有 ARP 条目

ip neigh show	#同arp -a,显示内网设备(邻居)
-add <IP> lladdr <MAC> dev <接口>	#新增静态条目
	sudo ip neigh add 192.168.1.100 lladdr 00:11:22:33:44:55 dev eth0	#示例:新增静态 ARP

sudo ip neigh del 192.168.1.100 dev eth0	#删除特定条目
sudo ip neigh flush dev eth0				#清除接口所有 ARP
------------------
#ip route 查看和管理路由表，用于内网/互联网流量控制
ip route show	#查看所有路由列表
-add <网络/掩码> via <网关> dev <接口>	#新增路由
	sudo ip route add 192.168.2.0/24 via 192.168.1.1 dev eth0	#示例:新增内网路由
-del <网络/掩码>	#删除路由
	sudo ip route del 192.168.2.0/24	#示例: 删除路由
-replace <网络/掩码> via <新网关>		#修改路由
	sudo ip route replace 192.168.2.0/24 via 192.168.1.2	#示例:修改路由
-------------------
nmcli connection show		#显示所有连接
```

#### 互联网管理

```sh
#ping 测试主机连通性
ping 192.168.1.1	#单个内网网关测试（无限，直到 Ctrl+C）
ping -c 4 www.google.com	#测试 4 次互联网连通性
-i <间隔>	#间隔秒数。
-s <大小>	#数据包大小。
--------------
#traceroute 跟踪到目标的路由路径，用于诊断互联网链接问题
traceroute www.google.com	#显示到目标的路由列表和延迟
traceroute -n 8.8.8.8	#快速数字追踪
-m <最大跳>	#最大跳数
-n				#不解析主机名（数字输出,速度快)
--------------
#dig 查询 DNS 记录，用于互联网域名解析管理。
dig www.example.com	#查询域名 IP（详细）
-+short	#简短输出
	dig +short MX example.com	#示例:查看邮件记录列表
@<服务器>	#指定 DNS 服务器
	dig @8.8.8.8 A example.com	#示例:使用 Google DNS 查询单个 A 记录
ANY	#查询所有类型
	dig @8.8.8.8 ANY example.com

host 域名	#查询域名对应ip

#指定本机解析
/etc/hosts
-------------
nmcli radio			#查看无线状态
nmcli radio wifi	#查看wifi
wifi connect <SSID> password <密码>	#连接（新增）
	nmcli device wifi connect MyWiFi password 'pass123'	#示例:新增并连接 SSID
	
---------------
#网络服务状态
systemctl status networking
```

#### 网络连接情况

```sh
#ss （推荐取代 netstat）显示网络连接、端口和套接字，用于查看活跃链接和任务
ss -tunlp	#查看端口开放
-t 	表示列出TCP协议的信息
-u	表示列出UDP协议的信息
-n	表示数字方式显示IP和端口
-l	表示只列出监听状态的网络连接
-p 	表示列出占用该端口的进程信息

netstat	-antp	#查看网络连接信息
--------------------
sudo lsof -i		#查看所有网络连接列表
sudo lsof -i :80	#查看单个 80 端口进程
sudo lsof -i TCP	#查看 TCP 连接

```

#### 防火墙

```sh
#防火墙
#说明debian12没有iptables，默认的是nftables
systemctl status nftables.service	#查看状态，默认未开启
systemctl enable nftables.service

#----- ufw（ufw是iptables的简洁化前端）
sudo ufw status	#(debian用)，查看防火墙状态	先安装ufw
sudo ufw enable		#开启防火墙
sudo ufw default deny 	#关闭所有外部对本机的访问，但本机访问外部正常
sudo ufw disable		#关闭防火墙
sudo ufw allow 80		#允许外部访问80端口
sudo ufw delete allow 80 	#禁止外部访问80 端口
sudo ufw allow from 192.168.1.1	#允许ip访问
sudo ufw deny smtp 		#禁止外部访问smtp服务
#------
```

### 任务计划

#### at

```sh
#在未来某个时间执行一次任务 
# 安装命令: sudo apt install at
#确保 atd 服务已启动。可通过 systemctl status atd 查看
#权限 /etc/at.allow 和 /etc/at.deny 文件可以限制哪些用户有权使用 at 命令。

#先输入at命令,然后在交互界面输入要执行的命令:
at 时间		
	#时间格式 HH:MM, DD.MM.YY MM/DD/YY 或 
	#相对时间:now+#[minutes，hours，days，weeks]
at> COMMAND		#在交互界面输入命令

#管道方式执行
echo "sh /root/script.sh" | at 23:00	#示例
echo "sh /root/script.sh" | at 23:00 ,2026-05-20	#示例
# -f 参数:直接执行脚本文件内容
at 04:00 PM tomorrow -f my_task.sh	#明天下午4点

#查询当前等待执行的任务及id
at -l		# 或atq
#删除
at -d [ID]
#查看具体内容
at -c [ID]
```

#### systemd-run

```sh
是 Linux 原生替代 at 的首选
#10分钟后执行一次任务
systemd-run --user --on-active=10min /home/user/myscript.sh
#30秒后
systemd-run --user --on-active=30s /usr/bin/touch /tmp/hello
#在特定时间执行：
systemd-run --user --on-calendar="2026-05-20 15:30:00" /usr/bin/touch /tmp/testfile

#查看
systemctl --user list-timers	#查看所有

#取消
systemctl --user stop run-u123.timer	#取消 "run-u123.timer"
```

#### cron

```sh
#周期性的执行某个任务 (已分钟为单位)
#cron自身是一个不间断运行的服务：crond
#查看服务: sudo systemctl status cron
=========================
#cron 的配置存储在名为 /etc/crontab 的文件中。
编辑任务：crontab -e（初次使用会让你选编辑器，建议选 nano 或 vim）
查看任务：crontab -l
删除所有任务：crontab -r
管理其他用户的任务（需 root）：sudo crontab -u 用户名 -e
=========================
#语法格式
 ┌───────────── 分钟 (0 - 59)
 │ ┌─────────── 小时 (0 - 23)
 │ │ ┌───────── 日 (1 - 31)
 │ │ │ ┌─────── 月 (1 - 12)
 │ │ │ │ ┌───── 星期 (0 - 6，0 是周日)
 │ │ │ │ │
 * * * * *  [要执行的命令]

*：匹配所有可能的值（每...）。
,：指定多个值（如 1,3,5 表示第1、3、5）。
-：指定范围（如 1-5 表示周一到周五）。
/：指定步长（如 */10 表示每隔10个单位）。

#示例:(必须使用绝对路径)
* * * * * /usr/bin/php /var/www/task.php	#每分钟执行一次
30 2 * * * /home/user/backup.sh				#每天凌晨 2:30 执行
0 * * * * /usr/bin/python3 /script.py		#每小时执行一次（整点）
0 */5 * * * /path/to/command				#每隔 5 小时的第 0 分钟执行
0 8 * * 1-5 /path/to/command				#每周一至周五的早上 8 点执行：
	
```

#### sleep

```sh
#Sleep + 后台运行（最简单的临时方案）
#示例bash代码:
(sleep 1h; /path/to/script.sh) &

#如果终端关闭或系统重启，任务会丢失。
```

### 日志系统

```sh
#syslog服务,包括2个进程：
syslogd：非内核其他设施产生日志
	/var/log/messages：系统标准错误日志信息
	/var/log/maillog：邮件系统产生的日志信息
	/var/log/secure：
klogd：内核产生日志 （记录到/var/log/dmesg）
```

```sh
/var/run/utmp		当前登录会话	#命令:w who users
/var/log/wtmp		历史登录记录	#命令:last	
/var/log/btmp		登录失败记录	#命令:lastb
/var/log/lastlog	每个用户最后登录时间	#命令:lastlog

~/.bash_history		命令历史	#命令:history
/var/log/auth.log	SSH相关日志	#命令:grep sshd /var/log/*

/var/log/messages 	系统综合日志 可能包含登录、sudo、su等记录	#命令:journalctl
```

```sh
#文本日志 (Logrotate)
清理周期：通常是 每周 (Weekly)。

#查看文本日志总大小
sudo du -sh /var/log

====================
#二进制日志 (Journald)
按空间占用清理:占用磁盘总量的 10% 左右，或者达到 4GB 时开

#查看当前日志占用总量
journalctl --disk-usage

#强制清理 Journal 日志（只保留最近 2 天）
sudo journalctl --vacuum-time=2d
# 示例:只保留最近 500M 的系统日志，其余自动删除
sudo journalctl --vacuum-size=500M
===================
dmesg -H	#内核缓冲日志,-H 人类可读
```

### 备份还原

```sh
rsync
```

