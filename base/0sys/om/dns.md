

#### dns

```sh
#域名解析
#绝大多数dns都是基于BIND软件构建

#自顶向下，层级管理，上级域知道下一级域，下级不知道上级
组织域：.com, .org, .net, .cc
国家域：.cn, .tw, .oq, .ir, .jp
反向域：IP->域名(FQDN)

#域名服务器，从根开始，逐层迭代查找，最后找到域名对应的ip地址
#如果查找范围在域名区域，则直接递归返回结果
#当外部客户端通过域名服务器解析时，只允许递归返回当前区域权威结果
#顶级域名不允许递归

#辅助dns服务器隔段时间请求主dns服务器保持同步
#如果主dns服务器没有反应，则辅dns服务器也会随之放弃解析
	serial number	#序列号
	refresh			#刷新时间
	retry			#重试时间
	expire			#过期时间
	negative answer TTL		#否定答案缓存时间
	
#缓存dns服务器
	仅提供缓存答案
	
#转发器

```

#### 资源记录

```sh
#数据库中，每一个条目称作一个资源记录(Rerource Record,RR)
$TTL 600;	#示例，可全局TTL设置600
#格式：
NAME 	[TTL]		IN		RRT		VALUE
www.xxx.com.		IN		A		1.1.1.1
1.1.1.1				IN		PTR		www.xxx.com.

#资源记录类型(RRT)
SOA		#Start of Authority，用于表明区域内部主从服务器如何同步数据以及起始对象,(出现在第一条)
	#格式：
	ZONE NAME		TTL		IN		SOA		FQDN	ADMINSTRATOR_MAINBOX	(serialnumber refresh retry expire nattl)
	#时间单位：M（分钟），H（小时），D（天），W（周），默认秒
	#邮箱格式：admin@xxx.com -> admin.xxx.com
	#示例：
	xxx.com.	600		IN		SOA		ns1.xxx.com		admin.xxx.com	2024100301 1H 5M 1W 1D
	
NS				#NAME Server,ZONE NAME->FQDN
	#示例：
	xxx.com.		600		IN		NS		ns.xxx.com.
	ns.xxx.com.		600		IN		A		1.1.1.2
A				#address,FQDN->IPv4，（主机名到ip都是A记录）
AAAA			#FQDN->IPv6
PTR				#pointer,IP->FQDN
MX				#Mail eXchanger,ZONE NAME->FQDN
	#格式示例：
	ZONE NAME		TTL		IN		MX		pri		value		#pri：优先级0-99，0最高
	xxx.com.		600		IN		MX		10		mail.xxx.com.
	mail.xxx.com.	600		IN		A				1.1.1.3
CNAME			#别名记录，FQDN->FQDN，（canonical name 正式名称）
	www2.xxx.com.		IN		CNAME		www.xxx.com.
TXT				#略
CHAOS			#略
SRV				#略
```

#### 域，区域

```sh
#正向区域文件示例：
@		IN		SOA					# @为简写方式
www		IN		A		192.168.0.1	# www为简写方式

#反向区域文件示例：
0.168.192.in-addr.arpa.		IN		SOA						#第一个字段为网段地址反着写
1.0.168.192.in-addr.arpa.	IN		PTR		www.xxx.com.
1							IN		PTR		www.xxx.com.	#简写方式


#区域传送：主从dns服务器传递数据

#区域类型：
	主区域：master
	从区域：slave
	提示区域：hint，定义根在什么地方
	转发区域：forward，明确指定目标dns，不需要从根去找
```

#### 搭建dns服务器

```sh
#使用命令：
apt install bind9		#debian系统
#或官网下载bind软件

#dns监听协议及端口：
	53/udp
	53/tcp
	953/tcp		#rndc监听（远程域名服务器控制器）

#服务名：named
#配置文件:/etc/named.conf
```

#### 域名解析工具

```sh
#dig工具，安装：略
#命令：略
	正向
	反向
	指定域名服务器
	区域传送
	
```

```sh
#host命令
host -t A www.baidu.com		#示例
```



