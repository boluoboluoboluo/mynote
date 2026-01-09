### 概要



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

#### 逻辑卷LVM

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



### 系统

#### 系统信息（debian为准）

```sh
#提权使用sudo，不建议使用root用户
#问题：xxx 不在 sudoers 文件中，此事将被报告。
#解决：
vi /etc/sudoers
#找到 # Allow members of group sudo to execute any command，在 %sudo ALL=(ALL:ALL) ALL 
#下面添加 xxx ALL=(ALL:ALL) ALL，xxx 为前面无法执行 sudo 命令的用户名

shutdown -r now	#重启	如提示未找到命令，则前面加 sudo
shutdown -r 10	#10分钟后重启
shutdown -h now	#关机
shutdown -h 10	#10分钟后关机

man 命令	#查看命令帮助
#快捷打开终端： `ctrl+alt+t`
#清屏幕：`ctrl+l` 或 命令clear

hostname 	#主机名 /etc/sysconfig/network
echo $HOSTNAME	#获取当前主机名
uname -a	#查看系统名
cat /proc/version	#查看版本的命令
cat /proc/cpuinfo	#查看cpu信息
cat /proc/meminfo	#查看内存信息
lscpu #cpu详细信息
lsusb	#查看usb设备
lspci	#查看所有设备信息

sudo su	#切换用户，（切换的用户并不是登录用户）
w		#查看当前系统中登录的用户,及正在干嘛
who 	#当前登录系统的用户
who -r	#显示当前运行级别
whoami	#当前用户
last	#最近登录及重启历史，显示的是/var/log/wtmp文件内容
	-n	#显示最近几次的登录，示例： last -n 3	#最近3次登录
lastb	#显示用户错误的登录尝试，/var/log/btmp内容
	-n	#显示最近，示例： lastb -n 3	#最近3次
lastlog	#每个用户上一次的登录
	-u	#显示特定用户，示例 lastlog -u test	#显示test用户上一次登录
basename	#
mail	#

date	#系统时间

free	#查看内存 -h 友好显示

top	#查看运行动态视图	
	# 按 e 内存可mb,gb,tb等友好显示
	# 按 shift+M 可以按内存大小排序

systemctl start 服务名		#启动服务
systemctl stop 服务名		#停止
systemctl restart 服务名		#重启
systemctl reload 服务名		#重载
systemctl enable 服务名		#自动启动
systemctl disable 服务名		#不自动启动
systemctl status 服务名		#查看运行的服务
systemctl list-units 服务名		#列出所有
systemctl list-units --type=service	#查看所有服务
systemctl list-units --type=service --state=running	#查看正在运行的服务
systemctl list-unit-files --type=service --state=enabled	#查看开机自启的服务

#锁屏快捷键
ctrl+alt+L

#锁终端
ctrl + S	#解锁:ctrl + Q

#终止进程
ctrl+c

#挂起进程
ctrl+z		#挂起当前进程到后台(占据内存-注意),使用jobs查看 
```

#### 环境变量

```sh
env :显示所有环境变量
set :显示本地定义的shell变量
export :把一个变量变作环境变量, 不加参数显示哪些变量导出为用户变量

#删除环境变量
unset varname

#相关文件
/etc/profile	#环境变量
/etc/bashrc		#shell变量

#====================
env		#查看当前用户全部环境变量
export	#当前系统定义的所有环境变量
echo $PATH		#查看path环境变量
#添加环境变量
sudo export PATH=/home/tuotu/bin:$PATH		#终端关闭失效
#第二种方法：
sudo vi /etc/profile
#在文档最后，添加:
export PATH="/home/tuotu/bin:$PATH"
#保存，退出，然后运行：
#source   /etc/profile
#即可
#====================

echo $LANG	#查看编码

echo $SHELL	#查看shell版本
```

#### 文件特殊权限

##### 文件访问权限

```sh
#文件权限
suid	#运行某程序时，相应进程的属主是程序文件自身的属主，而不是启动者
	chmod u+s file	#给文件添加s权限，若文件有x权限，显示为s，否则显示S
	此权限风险大，谨慎使用 
	示例：-rwsr-xr-x 1 root root 63736 7月  27  2018 /usr/bin/passwd
sgid	#属组，同上
sticky	#在一个公共目录，可以创建删除自己的文件，但不能删除别人的文件
	chmod o+t DIR	
	
#权限数字表示
100		#代表有s权限
示例：chmod 1755 filename	#前面的1代表具有sticky权限
示例：chmod 3755 filename	#前面的3代表具有suid权限和sticky权限
```

##### 文件额外访问控制权限FACL

```sh
#文件为file，属主和属组都是user1 权限750
#file user1 user1 
#若要是user2能访问file，又没有权限修改组权限，则需要用到FACL

#rwxr--r--+		#最后一个加号代表文件具有额外控制权限

#用法
getfacl filename	#查看文件的facl信息
setfacl 	#设置facl，说明：设置的权限不能超出facl中mask的权限范围
	-m	#设定
		u:uid:perm	#示例：setfacl -m u:test:rw file	#设置test用户对file具有rw权限
		g:gid:perm	#同上，组
		d:u:uid:perm	#前面的d代表目录（只能用于目录），表示为目录下文件自动继承该权限
		d:g:uid:perm	#同上，组
	-x	#取消	示例：setfacl -x u:test file	#取消test用户对file的额外控制权限
 	--mask	#设置mask 示例：setfacl --mask rw- file	#设置文件file的mask

#权限检查顺序
owner->facl,user->group->facl,group->other


```



### 用户

用户管理

```sh
id	#查看账号属性
finger username	#查看用户相关信息
change 	#修改用户属性信息
useradd [-cdgGsu] username	#添加用户，参数 -c：注释，-d：指定用户目录，-g：用户组
userdel username	#删除用户，参数 -r：连同用户主目录一并删除，

usermod username	#修改已有用户信息
	usermod -aG groupname username	#将用户添加到某个组

passwd [username]	#修改口令，普通用户修改自己，超级用户可修改其他用户口令，参数 -l：锁定，-u：解锁，-d：使账号无口令，-f：强迫下次登录修改口令

pwck 	#检查用户账户完整性

groupadd [-go] name	#添加用户组，参数 -g：指定标识号gid，-o：一般与g同时使用，表明新用户组与系统已有用户组的gid相同
groupdel name	#删除用户组
groupmod name	#修改用户组
newgrp groupname	#将当前用户临时切换到groupname的用户组，前提用户确实属于该用户组或附加组

/etc/passwd		#系统文件，记录用户基本属性，每行对应一个用户，含义=> 用户名:口令:用户标识号:组标识号:注释性描述:主目录:登录Shell
#口令字段存放的只是用户口令的加密串，不是明文，但是由于/etc/passwd文件对所有用户都可读，所以这仍是一个安全隐患。因此，现在许多Linux 系统（如SVR4）都使用了shadow技术，把真正的加密后的用户口令字存放到/etc/shadow文件中，而在/etc/passwd文件的口令字段中只存放一个特殊的字符，例如“x”或者“*”
#户标识号的取值范围是0～65 535。0是超级用户root的标识号，1～99由系统保留，作为管理账号，普通用户的标识号从100开始。在Linux系统中，这个界限是500。
#组标识对应着/etc/group文件中的一条记录。
#系统管理员可以根据系统情况和用户习惯为用户指定某个Shell。如果不指定Shell，那么系统使用sh为默认的登录Shell，即这个字段的值为/bin/sh。
#用户的登录Shell也可以指定为某个特定的程序（此程序不是一个命令解释器）。
#利用这一特点，我们可以限制用户只能运行指定的应用程序，在该应用程序运行结束后，用户就自动退出了系统。有些Linux 系统要求只有那些在系统中登记了的程序才能出现在这个字段中。

#系统中有一类用户称为伪用户（pseudo users）
#这些用户在/etc/passwd文件中也占有一条记录，但是不能登录，因为它们的登录Shell为空。它们的存在主要是方便系统管理，满足相应的系统进程对文件属主的要求。
#伪 用 户 含 义 
#bin 拥有可执行的用户命令文件 
#sys 拥有系统文件 
#adm 拥有帐户文件 
#uucp UUCP使用 
#lp lp或lpd子系统使用 
#nobody NFS使用

/etc/shadow
#登录名:加密口令:最后一次修改时间:最小时间间隔:最大时间间隔:警告时间:不活动时间:失效时间:标志

/etc/group
#组名:口令:组标识号:组内用户列表
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
chgrp [-R] 属组名 文件名	#更改文件属组，-R：递归更改文件属组
chown [–R] 属主名 文件名	#更改文件属主
chown [-R] 属主名：属组名 文件名

chmod [-R] xyz 文件或目录	#更改文件权限，r:4,w:2,x:1。xyz代表用户|组|其他的rwx值的和
chmod u=rwx,g=rx,o=r  test1    # 修改 test1 权限
chmod  a-x test1		#去掉可执行权限

umask	#遮罩码，用于创建文件的默认权限（默认值减遮罩码，即默认权限）文件默认值666，目录默认值777

ls 	#列出目录，参数 -a:全部文件，-d：仅列出目录，-l：列出文件属性详情，-i：显示inode节点信息
ls -lh	#查看目录详情


#cd中文目录
ls | nl		#列出目录编号
cd `ls | sed -n "xx,0p"`	#xx为目录的行号

pwd	[-P] #显示当前目录，参数 -P：显示确实路径，而不是链接(link)路径
mkdir [-mp]	目录名称	#创建目录，参数 -m：配置权限，-p：递归创建所需要的目录
rmdir [-p] 目录名		#删除空目录，参数 -p:从该目录起删除多级空目录

cp [-adfilprsu] src dst	#复制文件或目录，参数 -i：存在则询问，-p：连同属性一起复制，-r：递归复制，-d：若为链接，复制链接属性而非文件，-a:等于-pdr
rm [-fir] 文件或目录		#移除文件或目录，-f：强制，-i：询问，-r：递归
mv [-fiu] src dst	#移动文件或目录，或修改名称 参数-f：强制，-i：询问，-u：src文件较新则升级

cat [-AbEnTv] filename	#查看文件，参数 -A：列出特殊字符，-n：列出行号，-b：列出行号，空白行不显示行号
touch filename	#创建文件

#查找文件 参见bash
find 目录 -name '文件名'

#查看文件类型
file filename
```

```sh
#查看文件状态
stat filename

#文件有3个时间
#最后一次访问时间
#最后一次修改时间
#文件改变时间（属性）
#touch命令可修改文件的访问时间和修改时间

#less命令，查看文件，比more常用，可回翻
less filename

#tail命令
tail -f filename	#显示文件，默认10行，-f参数：实时显示文件添加的内容

#查看目录树
tree 

#排序
sort file	#目录下文件进行排序

#文本统计
wc file
cat file | wc -l	#统计行数

#字符转化
tr ”a" "A" < file	#文件里的a换成A
```

#### 压缩解压

```sh
tar		#归档压缩工具：打包 可压缩目录
	-c	#创建归档文件
	-f	file.tar	#指定归档后文件名
	-x	#展开归档
	--xattrs	#归档时保留文件扩展属性信息
	-t	#不展开，查看归档文件列表
	-zcf	#归档并调用gzip压缩
	-zxf	#gzip解压缩并展开归档，可省略z
	-jcf	#归档并调用bzip2压缩
	-jxf	#bzip2解压缩并展开归档，可省略j
	-Jcf	#归档并调用xz压缩
	-Jxf	#xz解压缩并展开归档，可省略J
	



#示例
#tar -czvf archive.tar.gz file1 file2 dir1
tar -czvf test.tar.gz a.c   #压缩 a.c文件为test.tar.gz
tar -tzvf test.tar.gz 		#列出压缩的文件
tar -xzvf test.tar.gz 		#解压文件

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

#xz 只能压缩文件，后缀.bz2 压缩更强悍
xz file	#压缩文件，生成file.xz，压缩后源文件被清除
	-d file.xz #解压缩，解压后file.xz被清除
	-num	#num为数字，1-9，指定压缩比，默认为6
	-k		#压缩后保留源文件

```

```sh
zip		#归档压缩,压缩后不删除源文件 压缩比小
zip file.zip file1 file2 ...	#压缩file1,file2...，到file.zip
unzip file.zip		#解压
unzip file.zip -d dir	#解压到目标文件夹

unzip -l file.zip 	#只看内容,不解压
unzip -o file.zip 	#强制覆盖已有文件(默认会询问)
unzip -n file.zip 	#不覆盖已有文件(跳过已存在的)
unzip -p "pass" file.zip 	#解压有密码的压缩包
```

```sh
cpio	#归档命令，同tar，不过更古老
```



### 磁盘

#### 磁盘操作命令

```sh
df [-ahikHTm] [目录或文件名]	#列出文件系统的整体磁盘使用量
# -a：列出所有，-k：以kb显示，-m：以mb显示，-h：以易阅读格式显示，-H：1000取消1024进位，-T：显示文件系统类型，-i：以inode数量显示

du [-ahskm] 文件或目录名称		#检查空间使用量
# -a：列出所有文件和目录容量，-h：易读格式，-s：列出总量，-S：不包括子目录的总计
du -h --max-depth=1		#列出当前目录各文件大小
du -sh .	#查看当前目录大小

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

##### 挂载

```sh
#查看挂载,相关命令：
mount
df -h
lsblk

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

##### 创建文件系统

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

```shell

#网络服务状态
systemctl status networking

ifconfig	#查看网络信息（旧命令）
ip addr		#(debian用)同上，如果上面命令未找到

#设置ip命令（本次设置有效）
ip addr add new_ip/mask dev ethx	#ethx：网卡名称
sudo ip link set dev ethx up	#使更改生效

#端口
netstat		#查看网络连接信息
ss  #(debian用)同上
ss -tunlp	
#-t表示列出TCP协议的信息
#-u表示列出UDP协议的信息
#-n表示数字方式显示IP和端口
#-l表示只列出监听状态的网络连接
#-p表示列出占用该端口的进程信息

host 域名	#查询域名对应ip
nslookup 域名	#同上

lsof	#命令是一种列出系统文件信息的命令，同时也可以列出进程信息，包括占用端口的进程信息。
sudo lsof -i :80 	#列出80端口的信息


#指定本机解析
/etc/hosts

#一块网卡可以有多个地址
eth0:0
eth0:1
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

### 进程

```sh
内核调度（进程管理结构表）
应用程序->进程（指令，堆栈，共享对象映射，变量，内存页框，上下文）
内存管理单元（MMU）
多核cpu
多进程，多线程（线程锁）
睡眠（场景：当执行的进程需要加载额外的io资源时，由于io速度慢，进程转入睡眠，交出cpu资源）
僵尸（进程运行结束，内存没有释放）->内存泄漏

进程优先级：
0-99：内核调整
100-139：用户可控制

进程间通信：（IPC）
	共享内存
	信号（Signal）
	Semaphore（旗语）

```

#### common

```sh
pstree	#进程树

ps -aux		#查看当前登录用户所有进程
	a:		#所有与终端有关的进程
	u:		#显示启动进程的用户信息
	x:		#所有与终端无关的进程
	
ps -ef		#列出进程及对应父进程
	e:		#显示所有进程
	f:		#所有格式

进程状态字段：
	D：不可中断的睡眠
	R：运行或就绪
	S：可中断的睡眠
	T：停止
	Z：僵死
	<：高优先级
	N：低优先级
	+：前台进程组中的进程
	l：多线程进程
	s：会话进程的首进程
	
top：	#进程动态显示
	M：根据驻留内存大小进行排序
	P：根据CPU使用百分比排序
	T：根据累计时间进行排序
	
	-d：指定延迟时长，单位秒
	-b：批模式
	-n #：在批模式，共显示多少批(#为数字，翻页)
	
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


#查看系统前10内存
ps -aux --sort=-%mem | head -11

#只看 PID、进程名和物理内存 RSS
ps -eo pid,comm,rss,%mem --sort=-rss | head -n 10		# -o 参数:指定格式

```

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

```sh
vmstat	#显示系统状态信息
vmstat 1 #每隔1秒显示1次
vmstat 1 5 #每隔1秒显示1次，共显示5次
```

### 任务计划

#### common

```sh
#1,未来的某个时间执行一次任务
	#at命令
	#语法：
		at 时间
			绝对时间：HH:MM, DD.MM.YY MM/DD/YY
			相对时间：now+#
				单位：minutes，hours，days，weeks
		at> COMMAND		#输入命令
		at> Ctrl+d		#结束命令
		
		at -ls		#显示at任务
		
		#权限
		/etc/at.deny
		
	#batch命令 （不需选择时间，自动选择系统空闲时执行），语法格式同at
	
#2，周期性的执行某个任务
	#cron命令 (cron自身是一个不间断运行的服务：crond)
		#系统cron，位于/etc/crontab
			#格式：分钟 小时 天 月 周 用户 任务
				#时间有效取值
				分钟：0-59
				小时：0-23
				天：1-31
				月：1-12
				周：0-7	（0和7都表示周日）
				#时间通配表示：
				*：对应所有有效取值
					13 12 * * *		#示例：每天12点13分
				,:离散时间点取值
                	10,40 * * * *	#示例，每小时第10分钟，第40分钟执行
                -：连续时间的
                	10 02 * * 1-5	#示例，周1到周5的2点10分
                /#：对应取值范围内每多久一次
                	*/3 * * * *		#示例，每3分钟一次
                
          	#执行结果以邮件形式发送给管理员
                */3 * * * * /bin/cat /etc/fstab &> /dev/null	#不发邮件
                */3 * * * * /bin/cat /etc/fstab > /dev/null	#仅错误结果发邮件
            #环境变量：PATH环境变量指定路径（/bin:/sbin:/usr/bin:/usr/sbin）
                	
		#用户cron，位于/var/spool/cron/USERNAME
			#格式：分钟 小时 天 月 周 任务
			#用户任务的管理
				crontab 
					-l:		#列出当前用户所有cron任务
					-e：		#编辑
					-r：		#移除
					-u USERNAME：		#管理其他用户的cron任务
			
			
	#anacron命令，cron的补充，能够实现cron实现因为各种原因(如关机)未执行的任务恢复执行一次
		#/etc/anacrontab
			1 65 cron.daily run-parts /etc/cron.daily	#示例，已经1天每执行，将在开机后65分钟执行

```

### 日志系统

#### common

```sh
#syslog服务,包括2个进程：
	syslogd：非内核其他设施产生日志
		/var/log/messages：系统标准错误日志信息
		/var/log/maillog：邮件系统产生的日志信息
		/var/log/secure：
	klogd：内核产生日志 （记录到/var/log/dmesg）
	
#日志滚动（日志切割）

#日志记录格式示例（/etc/syslog.conf）
mail.info /var/log/mail.log		#表示将mail相关，级别为info及以上的信息记录到/var/log/mail.log文件中
auth.=info @10.0.0.1			#表示将auth相关的，级别为info的信息记录到10.0.0.1主机上（该主机需配置配置文件）
user.!=error					#表示记录user相关，不包括error级别的信息
user.!error						#表示与user.error相反
*.info							#表示记录所有info及以上级别的信息
mail.*		-/var/log/mail.log	#记录mail相关的所有日志信息（异步写入）
*.*								#记录所有级别日志信息
cron.info;mail.info				#记录多个日志信息，cron和mail
cron,mail.info					#同上
mail.*;mail.!=info				#记录mail所有级别信息，不包括info级别
*.emerg		*					#emerg信息，立即发给所有用户

	
```

