```sh
核心：/boot/vmlinuz-version
内核模块（ko）：/libmodules/version/
```



#### 启动

```sh
POST -> BIOS(Boot Sequence) -> MBR(bootloader,446line) -> Kernel -> initrd -> /sbin/init（etc/inittab）

运行级别：0-6	#启动服务不同
	0：halt		#关机
	1：single user mode	#直接以管理员身份切入
	2：multi user mode	# no NFS（无网络）
	3：multi user mode，text mode	#命令行模式
	4：reserved	#保留，尚未使用
	5：multi user mode，graphic mode	#图形终端模式
	6：reboot	#重启
```

#### 详解启动过程

```sh
bootloader(MBR)
	LILO:Linux Loader
	GRUB:GRand Unified Bootloader
		Stage1:MBR
		Stage1_5:	#选择系统类型
		Stage2:/boot/grub
		
#内核初始化
1，硬件探测
2，装载驱动
3，挂载根文件系统
4，启动用户空间第一个进程init
```

```sh
#/etc/inittab的任务
1，设定默认运行级别
2，运行系统初始化脚本（/etc/rc.d/rc.sysinit）
3，运行指定运行级别对应目录下的脚本(/etc/rc.d/init.d)
4，设定ctrl+alt+del组合键的操作
5，定义ups电源故障/恢复时执行的操作
6，启动虚拟终端（级别2345）
7，启动图形终端（级别5）

#/etc/rc.d/rc.sysinit
1,检测并以读写方式重新挂载根文件系统
2，设定主机名
3，检测并挂载/etc/fstab中的其他文件系统
4，启动swap分区
5，初始化外围硬件设备的驱动
6，根据/etc/sysctl.conf设定内核参数
7，激活udev和selinux
8，激活LVM和RAID设备
9，清理过期锁和PID文件
10，装载键映射
```

#### 内核

```sh
#用户空间访问，监控内核方式
/proc		#伪文件系统，/proc/sys下很多文件可写
/sys		#伪文件系统，某些文件可写

#设定内核参数值的方法（临时立即生效）
echo VALUE > /proc/sys/FILE_NAME		#方法1，示例
sysctl -w kernel.hostname=STRING_VALUE	#方法2，示例

#设定内核参数值的方法（永久生效）
#修改/etc/sysctl.conf
# sysctl -p		#使修改立即生效
# sysctl -a		#显示所有内核参数及其值

lsmod	#列出内核装载的模块
modprobe MOD_NAME	#装载模块
modprobe -r MOD_NAME	#卸载模块
modeinfo MOD_NAME	#查看模块信息

insmod	/PATH/MOD_NAME	#装载模块，需指定模块路径
rmmod MOD_NAME	#移除模块
```

