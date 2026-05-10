

```sh
Linux 系统中最强大的命令行抓包工具,能实时截获并分析流经网卡的每一个数据包

#安装
sudo apt install tcpdump

#示例:(需要sudo权限)
tcpdump -i any		#查看所有网卡的流量, 流量高时不要轻易使用,会导致cpu负载飙升
tcpdump port 80		#查看80端口的流量
tcpdump src host 192.168.1.100	#只看某个 IP 发来的包
tcpdump src host 1.1.1.1 and port 80	#组合过滤（比如：来自 IP A 且 访问端口 80）
tcpdump -nn -i eth0	#查看网卡ech0的流量
tcpdump not port 22	#排除端口流量
tcpdump -c 10		#抓10个包
tcpdump -r output.pcap	#读取包文件
#参数:
-nn：直接显示 IP 和端口号，不要把它们解析成域名或服务名（速度更快，推荐）
-X：以十六进制和 ASCII 码显示包的内容（能看到具体的 HTTP 请求头等）
-w <文件名>.pcap：把抓到的包保存成文件
-r <文件名>.pcap：读取保存过的包文件

#建议使用:
在服务器上用 tcpdump -w test.pcap 抓包，然后把这个.pcap 用 Wireshark 图形化软件打开
```

