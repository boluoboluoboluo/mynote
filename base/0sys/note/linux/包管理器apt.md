#### 说明

```sh
# 1. apt和dpkg的关系
apt和dpkg都是Ubuntu上的包管理工具。apt是在dpkg外面套了一层壳，真正的安装，修改，删除，其实都是dpkg完成的

# 2.为什么每次使用apt更新前都先输入sudo apt update
因为Ubuntu的软件源中包含了大量包，直接搜索会给服务器造成较大的负担，所以apt采取的本地缓存策略，在本地保软件源的副本，每次用户需要更新其实都是在本地的这个副本查询。但软件源每天都在更新，所以每次在搜索和安装应用之前需要用apt update来同步一下本地副本。
```

```sh
#核心功能：
1，制作软件包
2，安装、卸载、升级、查询、校验
3，
```



#### apt

针对debian系列系统

```sh
#备份配置源
cp /etc/apt/sources.list /etc/apt/sources.list.bak
#配置清华源：清华源镜像站

# 默认注释了源码镜像以提高 apt update 速度，如有需要可自行取消注释
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ buster main contrib non-free
# deb-src https://mirrors.tuna.tsinghua.edu.cn/debian/ buster main contrib non-free
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ buster-updates main contrib non-free
# deb-src https://mirrors.tuna.tsinghua.edu.cn/debian/ buster-updates main contrib non-free
deb https://mirrors.tuna.tsinghua.edu.cn/debian-security buster/updates main contrib non-free
# deb-src https://mirrors.tuna.tsinghua.edu.cn/debian-security buster/updates main contrib non-free

#中科大源
deb https://mirrors.ustc.edu.cn/debian/ bullseye main contrib non-free
#deb-src https://mirrors.ustc.edu.cn/debian/ bullseye main contrib non-free
deb https://mirrors.ustc.edu.cn/debian/ bullseye-updates main contrib non-free
#deb-src https://mirrors.ustc.edu.cn/debian/ bullseye-updates main contrib non-free
deb https://mirrors.ustc.edu.cn/debian/ bullseye-backports main contrib non-free
#deb-src https://mirrors.ustc.edu.cn/debian/ bullseye-backports main contrib non-free
deb https://mirrors.ustc.edu.cn/debian-security/ bullseye-security main contrib non-free
#deb-src https://mirrors.ustc.edu.cn/debian-security/ bullseye-security main contrib non-free

```

```sh

#apt-get适合脚本，apt适合终端交互
apt-cache madison package_name	#查询源可用版本
sudo apt update		#更新
sudo apt search <keyword>	#查找
apt show <package_name>		#查看软件包的信息
sudo apt install <package_name>	
sudo apt install /full/path/file.deb		# 安装本地包
sudo apt remove <package_name>	
sudo apt autoremove		# 删除不需要的包（无依赖的）
sudo apt purge <package_name>	#移除软件包及配置文件
apt list --installed		#列出本地已安装的包
apt list --all-versions	#列出所有已安装的包的版本信息

#如果我们想安装一个软件包，但如果软件包已经存在，则不要升级它，可以使用 –no-upgrade 选项
sudo apt install <package_name> --no-upgrade	
#如果你想要从一个指定的源安装软件包，可以使用以下格式：
sudo apt -t stable install <package_name>	

#依赖相关
apt-cache depends package_name	#查看软件包的依赖关系
apt-cache rdepends package_name	#查看软件包的被依赖情况
#下面2条，更新软件包，并解决依赖
sudo get update
sudo get install -f


```

```sh
#说明：如果出现依赖关系问题，提示 依赖: libcurl4 (= 7.64.0-4+deb10u3) 但是 7.74.0-1.3+deb11u1 正要被安装
#解决方法：
sudo apt install libcurl4=7.64.0-4+deb10u3		#指定安装版本(降级)
```



#### dpkg

```sh
wget https://xxx/xxx.deb	#下载deb文件
$ dpkg -I xxx.deb # 查看安装包原数据信息摘要(-I == --info)
$ dpkg -c xxx.deb # 查看安装包原数据文件列表(-c == --contents)

#安装相关
dpkg -i package.deb		#安装或更新软件包
dpkg -r	package			#删除软件包
dpkg -s package			#查询软件包
dpkg -l					#列出已安装的软件包
dpkg -L package			#查询软件包的文件信息
dpkg -l package.deb		#查询软件包的依赖关系


#清理配置文件残留
dpkg -l |grep "^rc"|awk '{print $2}' |xargs aptitude -y purge
```

