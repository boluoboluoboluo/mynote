### samba共享

说明：linux和Windows共享基于cifs文件共享协议，使用smb协议通信，需要先在linux安装samba服务器。

另：nfs协议是linux和unix的标准文件系统，是为linux和unix环境文件共享而设计的



##### windows访问linux共享文件 

1. 安装samba服务器

   ```shell
   sudo apt update
   sudo apt install samba
   ```

2. 配置

   编辑`/etc/samba/smb.conf`在末尾添加以下内容：

   （默认可以访问用户目录，但只有读权限，如果限制访问用户目录，则清除此文件内容，添加下面内容即可）

   ```shell
   [share]
   comment = share directory
   path = /path	#共享目录
   browseable = yes
   read only = no
   guest ok = yes
   ```

3. 重启samba服务

   ```shell
   sudo systemctl restart smbd
   ```

4. 创建共享目录并设置权限

   ```shell
   sudo mkdir /path
   sudo chmod -R 777 /path		#根据实际情况配置
   ```

5. 为共享目录创建samba用户

   ```shell
   sudo smbpasswd -a dbn	# dbn为linux登录用户
   ```

6. windows访问共享文件夹

   命令行`win+r`，输入：\linux_ip

   输入用户名，密码



##### linux访问window共享文件

```shell
 #windows系统的目录share启用共享
 #linux系统/mnt目录下新建wshare目录，用于挂载
 #挂载命令，接着输入window用户的密码
 mount -t cifs -o username=windowsusername //windows_ip/share /mnt/wshare
```

```shell
#如果是linux虚拟机(我的是debian12)，主机是windows，需要安装vmare-tools工具，
#然后虚拟机设置-选项-共享文件夹，添加共享文件夹
#虚拟机/mnt下有hgfs目录，没有则创建
sudo vmhgfs-fuse ,host:/ /mnt/hgfs	#挂载命令
```



##### 备注

1. 确保机器能ping通
2. linux防火墙允许samba服务器端口通过
3. 如果无法访问，请尝试重启