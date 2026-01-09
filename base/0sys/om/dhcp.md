#### 地址分配

```sh
#dhcp基于udp协议工作
	服务端：67/udp
	客户端：68/udp

#dhcp地址分配过程：
1.客户端广播（需要IP地址）
	client->DHCPDISCOVER
2.dhcp服务器广播（分配IP地址）
	server->DHCPOFFER
3.客户端广播（已采用ip地址）
	client->DHCPREQUEST
4.dhcp服务器广播（知道了）
	server->DHCPACK
	
#续租
客户端单播：client->DHCPREQUETS
dhcp单播：server->DHCPACK

#如续租不成功，在租约的一半期限再次发起续租
#如续租始终不成功，则重新发起dhcp地址请求

```

#### 跨网段分配

```sh
# 路由器R，A网络有dhcp服务器Ad，B网络没有dhcp服务器，B网络主机b需要分配地址
# 则路由器可配置dhcp中继器（DHCP Relay）实现地址分配
#注意：dhcp服务器Ad的本地地址池和给B网络分配ip的地址池是分开的
b广播需要地址
R单播给Ad，需要地址
Ad单播给R，分配地址
R广播B网络，分配地址
b广播，采用地址
R单播Ad，采用地址
Ad单播R，确认
R广播B网路，确认
```

#### 保留地址

```sh
#dhcp保留地址用于分配静态地址，不属于地址池
```

#### 安装dhcp服务器

```sh
#查看
apt list | grep dhcp
#安装
apt install isc-dhcp-server

#配置文件：/etc/dhcp/dhcpd.conf
#配置：略
```

