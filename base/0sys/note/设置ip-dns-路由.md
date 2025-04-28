## windows

### 设置ip

```sh
#查看ip
ipconfig /all

#动态ip设置示例
netsh interface ip set address name="本地连接" source=dhcp
#静态ip设置示例
netsh interface ip set address name="本地连接" source=static addr=192.168.1.2 mask=255.255.255.0 gateway=192.168.1.1 gwmetric=auto

#参数说明：
-name：网络连接名称 一般为本地连接
-source：获取ip的途径。static：手动，dhcp：动态
-addr：要设置的ip地址
-mask：子网掩码
-gateway：网关地址
-gwmetric：网关跃点数，可设置整数值，也可设置为auto “自动”

#关闭网络连接
netsh interface set interface "本地连接" admin=disable
#开启
netsh interface set interface "本地连接" admin=enable
```



### 设置dns

```sh
#查看
ipconfig /all

#首选dns设置示例
netsh interface ip set dns name="本地连接" source=static addr=8.8.8.8 register=primary
#设置备用dns
netsh interface ip set dns name="本地连接" source=static addr=114.114.114.114 index=2

#参数说明：
-name：网络连接名称 一般为本地连接
-source：获取dns的途径。static：手动，dhcp：动态
-addr：要设置的dns地址
-register：注册方式。（None 禁用动态dns注册；primary 只在主dns后缀下注册；both 在主dns也在特定连接后缀下注册
-index：dns的序号

```



### 设置路由

 ```sh
#查看
route print
#删除单条路由
route delete 192.168.4.0 (网络地址)
#删除全部路由
route delete *

#设置语句格式
route add [-p] 目标地址 mask 子网掩码 网关地址 [metric 数字(1~9999)] 
#示例
route  -p  add 192.168.4.0 mask 255.255.255.0 192.168.1.1

#说明：
-目标地址：即目标路由地址
-网关地址：即当前需要添加路由的网口地址
-p ：此参数表示永久路由
-metric：可选参数,活动路由的(跃点数)值比永久路由的metric值大10。
 ```



### 其他

**重启服务** 

```sh
ipconfig /release	#释放ip
#或
ipconfig /renew		#更新ip地址

#或
netsh int ip reset	#重置tcp/ip协议
```

**删除0.0.0.0网关** 

```sh
route delete 0.0.0.0
```

**显示邻居** 

```sh
arp -a  #通信的计算机
```



## linux

> 系统：debian12



### 设置ip

```sh
#查看ip
ip addr
#查看网关
ip route	#defautl via 即网关

#查看网络接口状态
ip link
```

**静态设置：** 

备份原有配置文件`cp /etc/network/interfaces /etc/network/interfacesbak` 

编辑网网卡配置文件：`nano /etc/network/interfaces`，如下：

```sh
auto lo
iface lo inet loopback

auto eth0 #开机自动连接网络
iface eth0 inet static #static表示使用固定ip，dhcp表述使用动态ip
address 192.168.21.166 #设置ip地址
netmask 255.255.255.0 #设置子网掩码
gateway 192.168.21.2 #设置网关
```

保存退出。

**动态设置：** 

编辑网网卡配置文件：`nano /etc/network/interfaces`，如下：

```sh
auto lo
iface lo inet loopback

auto eth0 #开机自动连接网络
iface eth0 inet dhcp #static表示使用固定ip，dhcp表述使用动态ip
```

**开启指定网卡：** 

```sh
sudo ifup eth0
#或
ip link set eth0 up
```

**关闭指定网卡：** 

```sh
sudo ifdown eth0
#或
ip link set eth0 down
```



### 设置dns

备份原有dns配置文件`cp /etc/resolv.conf /etc/resolv.confbak`

编辑配置文件:`nano /etc/resolv.conf`，如下：

```sh
nameserver 8.8.8.8 #设置首选dns
nameserver 8.8.4.4 #设置备用dns
```

保存退出。



### 设置路由

**查看路由** 

```sh
#查看路由
ip route show
```

**临时路由** 

```sh
#添加临时路由
sudo ip route add <目标网段> via <网关地址> dev <接口名称>
```

**静态路由** 

备份原有配置文件`nano /etc/network/interfaces /etc/network/interfacesbak` 

编辑网网卡配置文件：`nano /etc/network/interfaces`，示例如下：

```sh
auto eth0
iface eth0 inet static
address 192.168.1.1
netmask 255.255.255.0
gateway 192.168.0.1
post-up ip route add 192.168.1.0/24 via 192.168.0.1	#此句配置静态路由
```

保存退出。

**删除路由** 

```sh
#删除路由
ip route del 192.168.2.0/24 via 192.168.1.1
#清空指定网络的路由
ip route flush 192.168.2.0/24 #这个是清理所有192.168.2.0/24相关的所有路由
```

### 其他

**重启dhcp客户端** 

```sh
sudo dhclient -r && sudo dhclient
#或 
systemctl restart dhcpcd 	#dhcp服务端
```

**重启网络服务** 

```sh
systemctl restart networking
```

**显示邻居** 

```sh
ip neigh show
#清理邻居（arp），如果删除不了，把网卡关了再删
ip neigh flush all
```

**释放ip** 

```sh
sudo dhclient -x	#释放获取的ip
```

**刷新ip** 

```sh
ip addr flush dev eth0	#刷新
```

**设置了静态ip还会自动添加动态ip问题** 

```sh
#networking与NetworkManager冲突

#关闭NetworkManager
systemctl stop NetworkManager
systemctl disable NetworkManager
```





