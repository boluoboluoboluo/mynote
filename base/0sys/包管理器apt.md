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

```sh
#apt底层原理
1.同步“菜单”:它会读取 /etc/apt/sources.list 文件中的服务器地址，访问远程仓库的 Packages.gz 索引文件
2.流量通常在20~100m左右(取决于添加了多少源)。它只下载包含软件包名、版本号、依赖关系的文本压缩包，不下载软件本身
3.本地处理：下载后,apt会在本地 /var/lib/apt/lists/ 目录下解析这些文本，构建一个庞大的本地数据库（包含成千上万个包的关系网）
4.目的:它让你的系统知道：现在云端有哪些新软件？旧软件有没有新版本？

#依赖树
某个软件安装运行需要的其他软件(xx版本xx软件等.)
#孤儿包
apt内部为每个包维护一个标记。如果是被作为依赖自动装进来的，它会被标记为“自动安装”。当没有其他手动安装的软件指向它时，它就变成了“孤儿包”。会被提示使用 apt autoremove 清理
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
sudo apt update		#更新源
apt-cache madison package_name	#查询源可用版本

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



#### 其他

```sh
#多个版本软件包共存

#共存的本质是“避开同名文件路径”。只要两个版本的软件不抢同一个 /usr/bin/ 下的文件名，不抢同一个 /lib/ 下的库名，不抢同一个端口（如果是服务），它们就能在同一台机器上平安无事

#软件包共存方式
1.建议使用 Docker 或 虚拟环境
2.原生安装,避开apt
```

```sh
#依赖关系

#依赖关系的底层是程序逻辑的碎片化。操作系统通过动态链接技术，在程序运行的瞬间，把分布在各处的碎片临时拼凑成一个完整的、可执行的实体

系统级依赖
运行环境依赖
库依赖
业务依赖
```

